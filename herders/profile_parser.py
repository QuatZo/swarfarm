from dateutil.parser import *
from django.utils.timezone import get_current_timezone
from jsonschema.exceptions import best_match

from bestiary.models import Monster, GameItem, LevelSkill
from herders.models import MonsterInstance, RuneInstance, RuneCraftInstance, MonsterPiece, ArtifactInstance, ArtifactCraftInstance, Summoner, LevelSkillInstance
from herders.profile_schema import HubUserLoginValidator, VisitFriendValidator

default_import_options = {
    'clear_profile': False,
    'default_priority': '',
    'lock_monsters': True,
    'minimum_stars': 1,
    'ignore_silver': False,
    'ignore_material': False,
    'except_with_runes': True,
    'except_light_and_dark': True,
    'except_fusion_ingredient': True,
    'delete_missing_monsters': 1,
    'delete_missing_runes': 1,
    'ignore_validation_errors': False
}


def validate_sw_json(data, summoner):
    validation_errors = []

    # Determine if it's a friend visit or a personal data file
    if 'friend' in data:
        validator = VisitFriendValidator
    else:
        validator = HubUserLoginValidator

    # Check the submitted data against a schema and return any errors in human readable format
    schema_error = best_match(validator.iter_errors(data))

    if schema_error:
        schema_error = 'Error in field {}:\n{}'.format(
            '[%s]' % ']['.join(repr(index) for index in schema_error.path),
            schema_error.message
        )
    else:
        # Do some supplementary checking
        if 'friend' in data:
            wizard_id = data['friend']['unit_list'][0]['wizard_id']
        else:
            wizard_id = data['wizard_info']['wizard_id']

        # Check that the com2us ID matches previously imported value
        if summoner.com2us_id is not None and summoner.com2us_id != wizard_id:
            validation_errors.append(
                'Uploaded data does not match account from previous import. Are you sure you want to upload this file?')

    return schema_error, validation_errors


def parse_sw_json(data, owner, options):
    wizard_id = None
    parsed_runes = {'to_update': {}, 'to_create': {}}
    parsed_rune_crafts = {}
    parsed_artifacts = {'to_update': {}, 'to_create': {}}
    parsed_artifact_crafts = {}
    parsed_mons = {}
    parsed_inventory = {}
    parsed_monster_shrine = {}
    parsed_monster_pieces = []
    parsed_level_skills = {}

    base_monsters = {m.com2us_id: m for m in Monster.objects.order_by().only('com2us_id', 'archetype', 'can_awaken', 'element', 'fusion_food')}
    owner_monsters = {}
    owner_runes = {}
    owner_artifacts = {}
    owner_rune_crafts = {}
    owner_artifact_crafts = {}

    if not options['clear_profile']:
        owner_monsters = {m.com2us_id: m for m in MonsterInstance.objects.filter(owner=owner).order_by()}
        owner_runes = {r.com2us_id: r for r in RuneInstance.objects.filter(owner=owner).order_by()}
        owner_artifacts = {a.com2us_id: a for a in ArtifactInstance.objects.filter(owner=owner).order_by()}
        owner_rune_crafts = {r.com2us_id: r for r in RuneCraftInstance.objects.filter(owner=owner).order_by()}
        owner_artifact_crafts = {a.com2us_id: a for a in ArtifactCraftInstance.objects.filter(owner=owner).order_by()}

    server_id_mapping = {
        None: None,
        1: Summoner.SERVER_GLOBAL,
        2: Summoner.SERVER_KOREA,
        3: Summoner.SERVER_JAPAN,
        4: Summoner.SERVER_CHINA,
        5: Summoner.SERVER_ASIA,
        6: Summoner.SERVER_EUROPE,
    }
    
    server_id = server_id_mapping[data.get('server_id', None)]

    # Grab the friend
    if data.get('command') == 'VisitFriend':
        data = data['friend']

    if 'wizard_info' in data:
        wizard_id = data['wizard_info'].get('wizard_id')

    building_list = data['building_list']
    level_skills = data['wizard_skill_list']  # Optional
    inventory_info = data.get('inventory_info')  # Optional
    unit_list = data['unit_list']
    runes_info = data.get('runes')  # Optional
    locked_mons = data.get('unit_lock_list')  # Optional
    craft_info = data.get('rune_craft_item_list')  # Optional
    artifact_info = data.get('artifacts')  # Optional
    artifact_craft_info = data.get('artifact_crafts')  # Optional
    monster_shrine_info = data.get('unit_storage_list')  # Optional

    if isinstance(level_skills, dict):
        level_skills = list(level_skills.values())
    
    for lvl_skill in level_skills:
        try:
            base_lvl_skill = LevelSkill.objects.get(com2us_id=lvl_skill['skill_id'])
        except LevelSkill.DoesNotExist:
            continue

        level = lvl_skill['level']

        try:
            lvl_skill_instance = LevelSkillInstance.objects.get(
                owner=owner, level_skill=base_lvl_skill)
        except LevelSkillInstance.DoesNotExist:
            lvl_skill_instance = LevelSkillInstance(
                owner=owner, level_skill=base_lvl_skill)
        except LevelSkillInstance.MultipleObjectsReturned:
            # Should only be 1 ever - use the first and delete the others.
            lvl_skill_instance = LevelSkillInstance.objects.filter(
                owner=owner, level_skill=base_lvl_skill).first()
            LevelSkillInstance.objects.filter(owner=owner, level_skill=base_lvl_skill).exclude(
                pk=lvl_skill_instance.pk).delete()
        if lvl_skill_instance.level != level:
            lvl_skill_instance.level = level
            parsed_level_skills[lvl_skill_instance.pk] = {
                'obj': lvl_skill_instance,
                'new': True,
            }
        else:
            parsed_level_skills[lvl_skill_instance.pk] = {
                'obj': lvl_skill_instance,
                'new': False,
            }

    # Buildings
    storage_building_id = None
    for building in building_list:
        if building:
            # Find which one is the storage building
            if building.get('building_master_id') == 25:
                storage_building_id = building.get('building_id')
                break

    # Inventory - essences and summoning pieces
    owner_pieces = {p.monster_id: p for p in MonsterPiece.objects.filter(owner=owner).order_by()}
    if inventory_info:
        for item in inventory_info:
            # Essence Inventory
            if (
                item['item_master_type'] == GameItem.CATEGORY_ESSENCE
                or item['item_master_type'] == GameItem.CATEGORY_CRAFT_STUFF
                or item['item_master_type'] == GameItem.CATEGORY_MATERIAL_MONSTER
                or item['item_master_type'] == GameItem.CATEGORY_ARTIFACT_CRAFT
            ):
                parsed_inventory[item['item_master_id']
                                 ] = item['item_quantity']
            elif item['item_master_type'] == GameItem.CATEGORY_MONSTER_PIECE:
                quantity = item.get('item_quantity')
                if quantity > 0:
                    mon = base_monsters.get(item['item_master_id'])

                    if mon:
                        has_changed = False
                        created = False
                        monster_piece = None
                        if owner_pieces:
                            monster_piece = owner_pieces.get(mon.pk)
                        else:
                            created = True
                            monster_piece = MonsterPiece(owner=owner, monster=mon, pieces=quantity)
                        
                        if not monster_piece:
                            continue

                        if not created and monster_piece.pieces != quantity:
                            monster_piece.pieces = quantity
                            has_changed = True
                        
                        parsed_monster_pieces.append({
                            'obj': monster_piece,
                            'new': has_changed or created,
                        })

    if monster_shrine_info:
        for item in monster_shrine_info:
            parsed_monster_shrine[item['unit_master_id']] = item['quantity']

    # Extract Rune Inventory (unequipped runes)
    if runes_info:
        for rune_data in runes_info:
            rune, to_update = parse_rune_data(rune_data, owner, owner_runes)
            if not rune:
                continue
            if to_update:
                parsed_runes['to_update'][rune.com2us_id] = rune
            else:
                parsed_runes['to_create'][rune.com2us_id] = rune

    # Extract monsters
    for unit_info in unit_list:
        # Get base monster type
        com2us_id = unit_info.get('unit_id')
        monster_type_id = unit_info.get('unit_master_id')
        mon = None

        if not options['clear_profile']:
            mon = owner_monsters.get(com2us_id, None)

        if not mon:
            mon = MonsterInstance()
            is_new = True
        else:
            is_new = False

        mon.com2us_id = com2us_id

        # Base monster
        temp_monster = base_monsters.get(monster_type_id, None)
        if not temp_monster:
            # Unable to find a matching monster in the database - either crap data or brand new monster. Don't parse it.
            continue

        # Equipped runes and artifacts
        equipped_runes = unit_info.get('runes')
        equipped_artifacts = unit_info.get('artifacts', [])

        # Sometimes the runes are a dict or a list in the json. Convert to list.
        if isinstance(equipped_runes, dict):
            equipped_runes = equipped_runes.values()

        mon_runes = []
        for rune_data in equipped_runes:
            rune, to_update = parse_rune_data(rune_data, owner, owner_runes)
            if not rune:
                continue
            if to_update:
                parsed_runes['to_update'][rune.com2us_id] = rune
            else:
                parsed_runes['to_create'][rune.com2us_id] = rune
            mon_runes.append(rune.com2us_id)

        mon_artifacts = []
        for artifact_data in equipped_artifacts:
            artifact = parse_artifact_data(artifact_data, owner, owner_artifacts)
            artifact, to_update = parse_artifact_data(artifact_data, owner, owner_artifacts)
            if not artifact:
                continue
            if to_update:
                parsed_artifacts['to_update'][artifact.com2us_id] = artifact
            else:
                parsed_artifacts['to_create'][artifact.com2us_id] = artifact
            mon_artifacts.append(artifact.com2us_id)

        skills = unit_info.get('skills', [])
        temp_skill_1_level = skills[0][1] if len(skills) >= 1 else None
        temp_skill_2_level = skills[1][1] if len(skills) >= 2 else None
        temp_skill_3_level = skills[2][1] if len(skills) >= 3 else None
        temp_skill_4_level = skills[3][1] if len(skills) >= 4 else None

        mon.monster = temp_monster
        mon.stars = unit_info.get('class')
        mon.level = unit_info.get('unit_level')

        # Lock a monster if it's locked in game
        if options['lock_monsters']:
            mon.ignore_for_fusion = locked_mons is not None and mon.com2us_id in locked_mons

        if temp_skill_1_level:
            mon.skill_1_level = temp_skill_1_level
        if temp_skill_2_level:
            mon.skill_2_level = temp_skill_2_level
        if temp_skill_3_level:
            mon.skill_3_level = temp_skill_3_level
        if temp_skill_4_level:
            mon.skill_4_level = temp_skill_4_level

        try:
            created_date = get_current_timezone().localize(
                parse(unit_info.get('create_time')), is_dst=False)
            mon.created = created_date
        except (ValueError, TypeError):
            mon.created = None

        mon.owner = owner
        mon.in_storage = unit_info.get('building_id') == storage_building_id

        # Set priority levels
        if options['default_priority'] and is_new:
            mon.priority = options['default_priority']

        if mon.monster.archetype == Monster.ARCHETYPE_MATERIAL:
            mon.fodder = True
            mon.priority = MonsterInstance.PRIORITY_DONE

        # Check import options to determine if monster should be saved
        level_ignored = mon.stars < options['minimum_stars']
        silver_ignored = options['ignore_silver'] and not mon.monster.can_awaken
        material_ignored = options['ignore_material'] and mon.monster.archetype == Monster.ARCHETYPE_MATERIAL
        allow_due_to_runes = options['except_with_runes'] and (
            len(equipped_runes) > 0 or len(equipped_artifacts) > 0)
        allow_due_to_ld = options['except_light_and_dark'] and mon.monster.element in [
            Monster.ELEMENT_DARK, Monster.ELEMENT_LIGHT] and mon.monster.archetype != Monster.ARCHETYPE_MATERIAL
        allow_due_to_fusion = options['except_fusion_ingredient'] and mon.monster.fusion_food

        should_be_skipped = any(
            [level_ignored, silver_ignored, material_ignored])
        import_anyway = any(
            [allow_due_to_runes, allow_due_to_ld, allow_due_to_fusion])

        if should_be_skipped and not import_anyway:
            continue

        # Set custom name if homunculus
        custom_name = unit_info.get('homunculus_name')
        if unit_info.get('homunculus') and custom_name:
            mon.custom_name = custom_name

        parsed_mons[mon.com2us_id] = {"obj": mon, "runes": mon_runes, "artifacts": mon_artifacts, "is_new": is_new}

    # Extract grindstones/enchant gems
    if craft_info:
        for craft_data in craft_info:
            craft, has_changed_or_new = parse_rune_craft_data(craft_data, owner, owner_rune_crafts)
            if craft:
                if has_changed_or_new:
                    craft.owner = owner
                parsed_rune_crafts[craft.pk] = {
                    'obj': craft,
                    'new': has_changed_or_new
                }

    # Extract artifact inventory
    if artifact_info:
        for artifact_data in artifact_info:
            artifact, to_update = parse_artifact_data(artifact_data, owner, owner_artifacts)
            if not artifact:
                continue
            if to_update:
                parsed_artifacts['to_update'][artifact.com2us_id] = artifact
            else:
                parsed_artifacts['to_create'][artifact.com2us_id] = artifact

    if artifact_craft_info:
        for craft_data in artifact_craft_info:
            craft, has_changed_or_new = parse_artifact_craft_data(craft_data, owner, owner_artifact_crafts)
            if craft:
                if has_changed_or_new:
                    craft.owner = owner
                parsed_artifact_crafts[craft.pk] = {
                    'obj': craft,
                    'new': has_changed_or_new,
                }

    import_results = {
        'wizard_id': wizard_id,
        'server_id': server_id,
        'monsters': parsed_mons,
        'monster_pieces': parsed_monster_pieces,
        'runes': parsed_runes,
        'rune_crafts': parsed_rune_crafts,
        'artifacts': parsed_artifacts,
        'artifact_crafts': parsed_artifact_crafts,
        'inventory': parsed_inventory,
        'monster_shrine': parsed_monster_shrine,
        'rta_assignments': data['world_arena_rune_equip_list'],
        'rta_assignments_artifacts': data['world_arena_artifact_equip_list'],
        'level_skills': parsed_level_skills,
    }

    return import_results


def get_monster_from_id(com2us_id):
    try:
        return Monster.objects.get(com2us_id=com2us_id)
    except (TypeError, ValueError):
        raise ValueError(
            'Unable to find monster matching ID ' + str(com2us_id))
    except Monster.DoesNotExist:
        return None


def parse_level_skill_data(level_skill_data, owner):
    pass


def parse_rune_data(rune_data, owner, owner_runes=None):
    com2us_id = rune_data.get('rune_id')
    to_update = True

    rune = None
    if owner_runes is not None:
        rune = owner_runes.get(com2us_id, None)
    else:
        rune = RuneInstance.objects.filter(
            com2us_id=com2us_id, owner=owner).first()

    if not rune:
        rune = RuneInstance()
        to_update = False

    # Firstly, info that may say if rune has changed or not
    substats = rune_data.get('sec_eff', [])
    temp_substats = []
    temp_substat_values = []
    temp_substats_enchanted = []
    temp_substats_grind_value = []

    for substat in substats:
        substat_type = RuneInstance.COM2US_STAT_MAP[substat[0]]
        substat_value = substat[1]
        enchanted = substat[2] == 1 if len(substat) >= 3 else 0
        grind_value = substat[3] if len(substat) >= 4 else 0

        temp_substats.append(substat_type)
        temp_substat_values.append(substat_value)
        temp_substats_enchanted.append(enchanted)
        temp_substats_grind_value.append(grind_value)

    # Basic rune info
    rune.type = RuneInstance.COM2US_TYPE_MAP[rune_data['set_id']]
    rune.com2us_id = com2us_id
    rune.value = rune_data.get('sell_value')
    rune.slot = rune_data.get('slot_no')
    stars = rune_data.get('class')
    if stars > 10:
        stars -= 10
        rune.ancient = True
    rune.stars = stars
    rune.level = rune_data.get('upgrade_curr')
    rune.original_quality = RuneInstance.COM2US_QUALITY_MAP.get(
        rune_data.get('extra'))

    # Rune stats
    main_stat = rune_data.get('pri_eff')
    if main_stat:
        rune.main_stat = RuneInstance.COM2US_STAT_MAP[main_stat[0]]
        rune.main_stat_value = main_stat[1]

    innate_stat = rune_data.get('prefix_eff')
    if innate_stat:
        rune.innate_stat = RuneInstance.COM2US_STAT_MAP.get(innate_stat[0])
        rune.innate_stat_value = innate_stat[1]

    rune.substats = temp_substats
    rune.substat_values = temp_substat_values
    rune.substats_enchanted = temp_substats_enchanted
    rune.substats_grind_value = temp_substats_grind_value

    rune.owner = owner
    rune.update_fields()

    return rune, to_update


def parse_rune_craft_data(craft_data, owner, owner_rune_crafts=None):
    # craft_type_id = 5 digit number
    # Work backwards to figure it out
    # [-1:] = quality
    # [-4:-2] = stat
    # [:-4] = rune set

    com2us_id = craft_data['craft_item_id']
    craft = None
    if owner_rune_crafts is not None:
        craft = owner_rune_crafts.get(com2us_id, None)
    else:
        craft = RuneCraftInstance.objects.filter(
            com2us_id=com2us_id, owner=owner).first()

    if not craft:
        is_new = True
        craft = RuneCraftInstance(com2us_id=com2us_id, owner=owner)
    else:
        is_new = False

    craft_type_id = str(craft_data['craft_type_id'])

    quality = int(craft_type_id[-1:])
    stat = int(craft_type_id[-4:-2])
    rune_set = int(craft_type_id[:-4])

    # if craft data already exists w/o quantity change, then we assume it's the same as it was before import
    if not is_new and craft.quantity == craft_data.get('amount', 1):
        return craft, False  # craft obj, has_changed_or_new

    craft.type = RuneCraftInstance.COM2US_CRAFT_TYPE_MAP.get(
        craft_data['craft_type'])
    craft.quality = RuneCraftInstance.COM2US_QUALITY_MAP.get(quality)
    craft.stat = RuneCraftInstance.COM2US_STAT_MAP.get(stat)
    craft.rune = RuneCraftInstance.COM2US_TYPE_MAP.get(rune_set)
    craft.quantity = craft_data.get('amount', 1)
    craft.value = craft_data['sell_value']

    return craft, True  # craft obj, has_changed_or_new


def parse_artifact_data(artifact_data, owner, owner_artifacts=None):
    com2us_id = artifact_data.get('rid')
    to_update = True

    artifact = None
    if owner_artifacts is not None:
        artifact = owner_artifacts.get(com2us_id, None)
    else:
        artifact = ArtifactInstance.objects.filter(
            com2us_id=com2us_id, owner=owner).first()

    if not artifact:
        artifact = ArtifactInstance(com2us_id=com2us_id, owner=owner)
        to_update = False

    temp_effects = []
    temp_effects_value = []
    temp_effects_upgrade_count = []
    temp_effects_reroll_count = []
    for sec_eff in artifact_data['sec_effects']:
        effect = artifact.COM2US_EFFECT_MAP[sec_eff[0]]
        value = sec_eff[1]
        upgrade_count = sec_eff[2]
        reroll_count = sec_eff[4]

        temp_effects.append(effect)
        temp_effects_value.append(value)
        temp_effects_upgrade_count.append(upgrade_count)
        temp_effects_reroll_count.append(reroll_count)

    # Basic artifact data
    artifact.slot = artifact.COM2US_SLOT_MAP[artifact_data['type']]
    if artifact.slot == artifact.SLOT_ELEMENTAL:
        artifact.archetype = None
        artifact.element = artifact.COM2US_ELEMENT_MAP[artifact_data['attribute']]
    else:
        artifact.element = None
        artifact.archetype = artifact.COM2US_ARCHETYPE_MAP[artifact_data['unit_style']]

    artifact.quality = artifact.COM2US_QUALITY_MAP[artifact_data['rank']]
    artifact.original_quality = artifact.COM2US_QUALITY_MAP[artifact_data['natural_rank']]
    artifact.level = artifact_data['level']

    # Stats and effects
    main_eff = artifact_data['pri_effect']
    artifact.main_stat = artifact.COM2US_MAIN_STAT_MAP[main_eff[0]]
    artifact.main_stat_value = main_eff[1]

    artifact.effects = temp_effects
    artifact.effects_value = temp_effects_value
    artifact.effects_upgrade_count = temp_effects_upgrade_count
    artifact.effects_reroll_count = temp_effects_reroll_count

    artifact.owner = owner
    artifact._update_values()

    return artifact, to_update


def parse_artifact_craft_data(craft_data, owner, owner_artifact_crafts=None):
    # master_id = 12 digit number
    # Digits:
    #   [0] = always 1, skip
    #   [1:3] = artifact type
    #   [3:5] = element
    #   [5:7] = unit archetype
    #   [7:9] = quality
    #   [9:] = effect

    com2us_id = craft_data['rid']
    if owner_artifact_crafts is not None:
        craft = owner_artifact_crafts.get(com2us_id, None)
    else:
        craft = ArtifactCraftInstance.objects.filter(
            com2us_id=com2us_id, owner=owner).first()

    if not craft:
        is_new = True
        craft = ArtifactCraftInstance(com2us_id=com2us_id, owner=owner)
    else:
        is_new = False

    craft_type_id = str(craft_data['master_id'])
    artifact_type = int(craft_type_id[1:3])
    unit_element = int(craft_type_id[3:5])
    unit_archetype = int(craft_type_id[5:7])
    quality = int(craft_type_id[7:9])
    effect = int(craft_type_id[9:])

    # if craft data already exists w/o quantity change, then we assume it's the same as it was before import
    if not is_new and craft.quantity == craft_data.get('amount', 1):
        return craft, False  # craft obj, has_changed_or_new

    craft.slot = ArtifactCraftInstance.COM2US_SLOT_MAP.get(artifact_type)
    craft.element = ArtifactCraftInstance.COM2US_ELEMENT_MAP.get(
        unit_element) if unit_element else None
    craft.archetype = ArtifactCraftInstance.COM2US_ARCHETYPE_MAP.get(
        unit_archetype) if unit_archetype else None
    craft.quality = ArtifactCraftInstance.COM2US_QUALITY_MAP.get(quality)
    craft.effect = ArtifactCraftInstance.COM2US_EFFECT_MAP.get(effect)
    craft.quantity = craft_data.get('amount', 1)

    return craft, True  # craft obj, has_changed_or_new
