from dataclasses import dataclass, field
from typing import Dict, Any, List, Literal

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TaskSchema:
    availability: Literal["all", "only_first", "all_except_first"] = "all"
    enabled: bool = False


@dataclass_json
@dataclass
class CordsSchema:
    x: int = 0
    y: int = 0


@dataclass_json
@dataclass
class CityCordsSchema(CordsSchema):
    kingdom: int = 0


@dataclass_json
@dataclass
class MinMaxSchema:
    min: int = 0
    max: int = 0

@dataclass_json
@dataclass
class NodeLimitSchema:
    enabled: bool = False
    fixed_node_limit: int = 0

@dataclass_json
@dataclass
class TaskGatherGemSchema(TaskSchema):
    duration: MinMaxSchema = field(default_factory=MinMaxSchema)
    searching_radius: int = 30
    node_limit: NodeLimitSchema = field(default_factory=NodeLimitSchema)
    compare_march_duration: bool = True

    search_method: Literal["default", "spiral", "map"] = "map"
    map_center_pos: CordsSchema = field(default_factory=CordsSchema)
    # scan_frequency: MinMaxSchema = MinMaxSchema(min=0,max=0)
    # city_cords: CityCordsSchema = field(default_factory=CityCordsSchema)
    # detect_free_marches_without_clicking_on_node = True
    # automatically_recenter: bool = True


@dataclass_json
@dataclass
class NodeChoiceSchema:
    type: Literal["food", "wood", "stone", "gold", "nothing"] = "food"
    level: int = 6


@dataclass_json
@dataclass
class TaskGatherRssSchema(TaskSchema):
    method: Literal["default", "spiral"] = "spiral"
    use_custom_preset: bool = False
    first_node: NodeChoiceSchema = field(default_factory=NodeChoiceSchema)
    second_node: NodeChoiceSchema = field(default_factory=NodeChoiceSchema)
    third_node: NodeChoiceSchema = field(default_factory=NodeChoiceSchema)
    fourth_node: NodeChoiceSchema = field(default_factory=NodeChoiceSchema)
    fifth_node: NodeChoiceSchema = field(default_factory=NodeChoiceSchema)
    sixth_node: NodeChoiceSchema = field(default_factory=NodeChoiceSchema)
    seventh_node: NodeChoiceSchema = field(default_factory=NodeChoiceSchema)


@dataclass_json
@dataclass
class TaskCollectCityResourcesSchema(TaskSchema):
    pass


@dataclass_json
@dataclass
class TaskApplyBuffSchema(TaskSchema):
    pass


@dataclass_json
@dataclass
class TaskBuyMysteriousMerchantSchema(TaskSchema):
    pass


@dataclass_json
@dataclass
class TaskDonateToAllianceSchema(TaskSchema):
    pass


@dataclass_json
@dataclass
class TaskAlliancePitSchema(TaskSchema):
    pass


@dataclass_json
@dataclass
class MaterialsChoiceSchema:
    type: Literal["leather", "iron", "stone", "wood", "food"] = "leather"


@dataclass_json
@dataclass
class TaskProduceMaterialsSchema(TaskSchema):
    first_choice: MaterialsChoiceSchema = field(default_factory=MaterialsChoiceSchema)
    second_choice: MaterialsChoiceSchema = field(default_factory=MaterialsChoiceSchema)
    third_choice: MaterialsChoiceSchema = field(default_factory=MaterialsChoiceSchema)
    fourth_choice: MaterialsChoiceSchema = field(default_factory=MaterialsChoiceSchema)
    fifth_choice: MaterialsChoiceSchema = field(default_factory=MaterialsChoiceSchema)


@dataclass_json
@dataclass
class TaskTroopTraining(TaskSchema):
    infantry_camp: CordsSchema = field(default_factory=CordsSchema)
    cavalry_camp: CordsSchema = field(default_factory=CordsSchema)
    archery_camp: CordsSchema = field(default_factory=CordsSchema)
    siege_camp: CordsSchema = field(default_factory=CordsSchema)


@dataclass_json
@dataclass
class TaskClaimDailyVipChestSchema(TaskSchema):
    pass


@dataclass_json
@dataclass
class TaskClaimDailyChestSchema(TaskSchema):
    pass


@dataclass_json
@dataclass
class TaskClaimDailyQuestSchema(TaskSchema):
    pass


@dataclass_json
@dataclass
class TaskClaimDailyExpeditionRewardsSchema(TaskSchema):
    enable_buy_heads: bool = False
    enable_buy_items: bool = False


@dataclass_json
@dataclass
class TaskClaimMailSchema(TaskSchema):
    pass


@dataclass_json
@dataclass
class TaskAllianceHelpSchema(TaskSchema):
    pass


@dataclass_json
@dataclass
class TaskKillBarbarianSchema(TaskSchema):
    target_level: int = 25
    enable_first_preset: bool = False
    enable_second_preset: bool = False
    enable_third_preset: bool = False
    enable_fourth_preset: bool = False
    enable_fifth_preset: bool = False
    enable_sixth_preset: bool = False
    enable_seventh_preset: bool = False


@dataclass_json
@dataclass
class TaskAllianceFortSchema(TaskSchema):
    skip_leader_back: bool = False
    mobilisation_time: Literal[5, 10, 30] = 5
    rally_type: Literal["inf", "cav", "archers"] = "cav"
    marauders_mode: bool = False


@dataclass_json
@dataclass
class TaskExploreFogSchema(TaskSchema):
    duration: MinMaxSchema = field(default_factory=MinMaxSchema)
    scout_camp_position: CordsSchema = field(default_factory=CordsSchema)


@dataclass_json
@dataclass
class TaskUpgradeCitySchema(TaskSchema):
    method: Literal["normal", "safest"] = "normal"
    city_hall_position: CordsSchema = field(default_factory=CordsSchema)


@dataclass_json
@dataclass
class TaskAcademicResearchSchema(TaskSchema):
    academy_position: CordsSchema = field(default_factory=CordsSchema)


@dataclass_json
@dataclass
class TaskTroopHealingSchema(TaskSchema):
    hospital_position: CordsSchema = field(default_factory=CordsSchema)
    healing_batch_size: int = 1500


@dataclass_json
@dataclass
class TaskResourcesTransferSchema(TaskSchema):
    fast_transfer: bool = False
    food_amount: int = 0
    wood_amount: int = 0
    stone_amount: int = 0
    gold_amount: int = 0


@dataclass_json
@dataclass
class AllowedTimeSlotsSchema:
    start: str
    end: str


@dataclass_json
@dataclass
class TaskLibrarySchema:
    gather_gem: TaskGatherGemSchema = field(default_factory=TaskGatherGemSchema)
    gather_rss: TaskGatherRssSchema = field(default_factory=TaskGatherRssSchema)
    collect_city_resources: TaskCollectCityResourcesSchema = field(default_factory=TaskCollectCityResourcesSchema)
    apply_buff: TaskApplyBuffSchema = field(default_factory=TaskApplyBuffSchema)
    buy_mysterious_merchant: TaskBuyMysteriousMerchantSchema = field(default_factory=TaskBuyMysteriousMerchantSchema)
    donate_to_alliance: TaskDonateToAllianceSchema = field(default_factory=TaskDonateToAllianceSchema)
    alliance_pit: TaskAlliancePitSchema = field(default_factory=TaskAlliancePitSchema)
    produce_materials: TaskProduceMaterialsSchema = field(default_factory=TaskProduceMaterialsSchema)
    troop_training: TaskTroopTraining = field(default_factory=TaskTroopTraining)
    claim_daily_vip_chest: TaskClaimDailyVipChestSchema = field(default_factory=TaskClaimDailyVipChestSchema)
    claim_daily_chest: TaskClaimDailyChestSchema = field(default_factory=TaskClaimDailyChestSchema)
    claim_daily_quest: TaskClaimDailyQuestSchema = field(default_factory=TaskClaimDailyQuestSchema)
    claim_daily_expedition_rewards: TaskClaimDailyExpeditionRewardsSchema = field(
        default_factory=TaskClaimDailyExpeditionRewardsSchema)
    claim_mail: TaskClaimMailSchema = field(default_factory=TaskClaimMailSchema)
    alliance_help: TaskAllianceHelpSchema = field(default_factory=TaskAllianceHelpSchema)
    kill_barbarian: TaskKillBarbarianSchema = field(default_factory=TaskKillBarbarianSchema)
    alliance_fort: TaskAllianceFortSchema = field(default_factory=TaskAllianceFortSchema)
    explore_fog: TaskExploreFogSchema = field(default_factory=TaskExploreFogSchema)
    upgrade_city: TaskUpgradeCitySchema = field(default_factory=TaskUpgradeCitySchema)
    academic_research: TaskAcademicResearchSchema = field(default_factory=TaskAcademicResearchSchema)
    troop_healing: TaskTroopHealingSchema = field(default_factory=TaskTroopHealingSchema)
    resources_transfer: TaskResourcesTransferSchema = field(default_factory=TaskResourcesTransferSchema)


@dataclass_json
@dataclass
class ProfileSchema:
    enabled: bool = False
    allowed_time_slots: List[AllowedTimeSlotsSchema] = field(default_factory=list)
    enable_time_slots: TaskSchema = field(default_factory=TaskSchema)

    enable_reconnect_on_error: bool = True
    enable_log_back_on_device_switch: bool = True
    log_back_on_device_switch_duration: MinMaxSchema = field(default_factory=MinMaxSchema)
    enable_captcha_solver: bool = True
    enable_switch_character: bool = True
    enable_switch_character_restart_during_game_load: bool = False
    enable_sleep_factor: bool = True
    sleep_factor: int = 1

    tasks: TaskLibrarySchema = field(default_factory=TaskLibrarySchema)

@dataclass_json
@dataclass
class EmulatorSettingsSchema:
    emulator: str = ""
    instance: str = ""
    name: str = ""
    host: str = ""
    port: int = 0
    # loop_task: bool = True
    # loop_duration: MinMaxSchema = field(default_factory=lambda: MinMaxSchema(min=60, max=120))
    # leave_game_loop: bool = True
    scheduler: bool = False
    schedules: Dict[str, ProfileSchema] = field(default_factory=lambda: {
        "1": ProfileSchema(),
        "2": ProfileSchema(),
        "3": ProfileSchema(),
    })

@dataclass_json
@dataclass
class EmulatorListSchema:
    emulators: Dict[str, EmulatorSettingsSchema] = field(default_factory=dict)


@dataclass_json
@dataclass
class EmulatorTypeSchema:
    emulator_type: Dict[str, EmulatorListSchema] = field(default_factory=dict)