from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import User

from herders.models import ArtifactInstance, RuneInstance, MonsterInstance, Summoner

import os
import json
import copy
import time
import random
import string

class Command(BaseCommand):
    help = 'Creates `accounts_quantity` accounts with propagated data from first Summoner.'
    MIN, MAX = 1, 1000000000

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            '-a',
            '--accounts_quantity',
            type=int,
            default=100,
            help='Number of accounts to create',
        )

    def handle(self, *args, **kwargs):
        # TODO: Add whole `herders` copy, not only Monsters, Runes & Artifacts
        # TODO: DEFAULT / RTA BUILDS
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR('Command used outside DEBUG Mode'))
            return

        # timestamp, so there's no problem with dupe account logins
        ACC_LOGIN = f'propagated_$ID$_{int(time.time())}'
        # some sort of PASSWD generator, we won't use it anyway
        PASSWD = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(24))

        monster_fields = [
            'pk', 'owner_id', 'monster_id', 'com2us_id', 'created', 'stars', 'level', 'skill_1_level', 'skill_2_level', 'skill_3_level', 'skill_4_level',
            'fodder', 'in_storage', 'ignore_for_fusion', 'priority', 'notes', 'custom_name',
        ]
        rune_fields = [
            'type', 'owner_id', 'com2us_id', 'assigned_to_id', 'marked_for_sale', 'notes', 'main_stat', 'main_stat_value',
            'innate_stat', 'innate_stat_value', 'stars', 'level', 'slot', 'quality', 'original_quality', 'ancient', 'value', 
            'substats', 'substat_values', 'substats_enchanted', 'substats_grind_value', 'has_hp', 'has_atk', 'has_def',
            'has_crit_rate', 'has_crit_dmg', 'has_speed', 'has_resist', 'has_accuracy', 'efficiency', 'max_efficiency',
            'substat_upgrades_remaining', 'has_grind', 'has_gem',
        ]
        artifact_fields = [
            'owner_id', 'com2us_id', 'assigned_to_id', 'level', 'original_quality', 'main_stat', 'main_stat_value',
            'effects', 'effects_value', 'effects_upgrade_count', 'effects_reroll_count', 'efficiency', 'max_efficiency',
            'slot', 'element', 'archetype', 'quality'
        ]

        start = time.time()
        acc_quantity = kwargs['accounts_quantity']
        self.stdout.write(self.style.SUCCESS(f'Starting data duplication process for {acc_quantity} account(s)!'))

        owner = Summoner.objects.first()
        if not owner:
            self.stdout.write(self.style.ERROR("No Summoner records in database, can't duplicate empty data"))
            return

        monsters = MonsterInstance.objects.filter(owner=owner).values(*monster_fields)
        runes = RuneInstance.objects.filter(owner=owner).values(*rune_fields)
        artifacts = ArtifactInstance.objects.filter(owner=owner).values(*artifact_fields)

        self.stdout.write(self.style.SUCCESS(f'Duplicating per account:'))
        self.stdout.write(self.style.WARNING(f'- Monsters: {len(monsters)}'))
        self.stdout.write(self.style.WARNING(f'- Runes: {len(runes)}'))
        self.stdout.write(self.style.WARNING(f'- Artifacts: {len(artifacts)}'))

        monster_pks = {m.pop('pk'): m['com2us_id'] for m in monsters}

        for iter in range(acc_quantity):
            iter_objs = {
                'monsters': [],
                'runes': [],
                'artifacts': [],
            }
            login = ACC_LOGIN.replace('$ID$', str(iter))
            iter_start = time.time()
            with transaction.atomic():
                user = User.objects.create_user(login, login + '@gmail.com', PASSWD)

                summoner = Summoner.objects.create(user=user, com2us_id=owner.com2us_id)

                for mon in monsters:
                    mon_obj = MonsterInstance(**mon)
                    mon_obj.owner = summoner
                    iter_objs['monsters'].append(mon_obj)

                iter_mons = {m.com2us_id: m for m in MonsterInstance.objects.bulk_create(iter_objs['monsters'])}

                for rune in runes:
                    rune_obj = RuneInstance(**rune)
                    rune_obj.owner = summoner
                    rune_obj.assigned_to = iter_mons[monster_pks[rune['assigned_to_id']]] if rune['assigned_to_id'] else None
                    iter_objs['runes'].append(rune_obj)

                for artifact in artifacts:
                    artifact_obj = ArtifactInstance(**artifact)
                    artifact_obj.owner = summoner
                    artifact_obj.assigned_to = iter_mons[monster_pks[artifact['assigned_to_id']]] if artifact['assigned_to_id'] else None
                    iter_objs['artifacts'].append(artifact_obj)

                RuneInstance.objects.bulk_create(iter_objs['runes'])
                ArtifactInstance.objects.bulk_create(iter_objs['artifacts'])
                
                self.stdout.write(self.style.WARNING(f"[{iter + 1}] This iteration took {round(time.time() - iter_start, 2)} seconds ({round(time.time() - start, 2)} in total)!"))
                
        self.stdout.write(self.style.SUCCESS('Done creating accounts and duplicating data.'))