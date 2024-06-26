import django_filters.rest_framework as filters

from .models import Monster, SkillEffect, Skill, LeaderSkill, ScalingStat


class MonsterFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name')
    element = filters.MultipleChoiceFilter(choices=Monster.ELEMENT_CHOICES)
    archetype = filters.MultipleChoiceFilter(choices=Monster.ARCHETYPE_CHOICES)
    awaken_level = filters.MultipleChoiceFilter(choices=Monster.AWAKEN_CHOICES)
    leader_skill_attribute = filters.MultipleChoiceFilter(field_name='leader_skill__attribute', choices=LeaderSkill.ATTRIBUTE_CHOICES)
    leader_skill_area = filters.MultipleChoiceFilter(field_name='leader_skill__area', choices=LeaderSkill.AREA_CHOICES)
    order_by = filters.OrderingFilter(fields=[
        'name', 'element', 'base_stars', 'natural_stars', 'archetype', 'com2us_id', 'family_id', 'skill_group_id',
        'raw_hp', 'raw_attack', 'raw_defense',
        'base_hp', 'base_attack', 'base_defense',
        'max_lvl_hp', 'max_lvl_attack', 'max_lvl_defense',
        'speed', 'crit_rate', 'crit_damage', 'resistance', 'accuracy',
    ])

    class Meta:
        model = Monster
        fields = {
            'id': ['in'],
            'com2us_id': ['exact'],
            'family_id': ['exact'],
            'skill_group_id': ['exact'],
            'base_stars': ['exact', 'lte', 'gte'],
            'natural_stars': ['exact', 'lte', 'gte'],
            'obtainable': ['exact'],
            'fusion_food': ['exact'],
            'homunculus': ['exact'],
        }

    def filter_name(self, queryset, name, value):
        if value:
            return queryset.filter(name__istartswith=value)
        else:
            return queryset


class SkillFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name')
    description = filters.CharFilter(method='filter_description')
    scaling_stats__pk = filters.ModelMultipleChoiceFilter(queryset=ScalingStat.objects.all(), to_field_name='pk', conjoined=True)
    effects_logic = filters.BooleanFilter(method='filter_effects_logic')
    effect__pk = filters.ModelMultipleChoiceFilter(queryset=SkillEffect.objects.all(), method='filter_effects')
    used_on = filters.NumberFilter(method='filter_used_on')

    class Meta:
        model = Skill
        fields = {
            'id': ['in'],
            'name': ['exact'],
            'com2us_id': ['exact'],
            'slot': ['exact'],
            'cooltime': ['exact', 'isnull', 'gte', 'lte', 'gt', 'lt'],
            'hits': ['exact', 'isnull', 'gte', 'lte', 'gt', 'lt'],
            'aoe': ['exact'],
            'passive': ['exact'],
            'max_level': ['exact', 'gte', 'lte', 'gt', 'lt'],
        }

    def filter_name(self, queryset, name, value):
        return queryset.filter(name__istartswith=value)

    def filter_description(self, queryset, name, value):
        return queryset.filter(description__icontains=value)

    def filter_effects(self, queryset, name, value):
        old_filtering = self.form.cleaned_data.get('effects_logic', False)
        stat_scaling = self.form.cleaned_data.get('scaling_stats__pk', [])

        if old_filtering:
            # Filter if any skill on the monster has the designated fields
            for effect in value:
                queryset = queryset.filter(effect=effect)

            for pk in stat_scaling:
                queryset = queryset.filter(scaling_stats=pk)

            return queryset.distinct()
        else:
            # Filter effects based on effects of each individual skill. This ensures a monster will not show up unless it has
            # the desired effects on the same skill rather than across any skills.
            skills = Skill.objects.all()

            for effect in value:
                skills = skills.filter(effect=effect)

            for pk in stat_scaling:
                skills = skills.filter(scaling_stats=pk)

            return queryset.filter(pk__in=skills).distinct()

    def filter_used_on(self, queryset, name, value):
        return queryset.filter(monster__pk=value)

    def filter_effects_logic(self, queryset, name, value):
        # This field is just used to alter the logic of skill effect filter
        return queryset
