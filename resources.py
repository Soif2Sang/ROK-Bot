from time import time

from cv2 import cvtColor, imread, matchTemplate, minMaxLoc, COLOR_BGR2RGB, TM_CCOEFF_NORMED, imdecode,         IMREAD_COLOR, COLOR_BGR2HSV, inRange
class ImageSingleton:
    __instance = None
    def __new__(cls):
       if cls.__instance is None:
           cls.__instance = super().__new__(cls)
           cls.__instance.load_images()
       return cls.__instance

    def load_images(self):
       self.academy= imread('resources\\academy.png')
       self.academy_tech= imread('resources\\academy_tech.png')
       self.alliance_flag1= imread('resources\\alliance_flag1.png')
       self.alliance_flag2= imread('resources\\alliance_flag2.png')
       self.alliance_gifts_claim_button= imread('resources\\alliance_gifts_claim_button.png')
       self.alliance_tech= imread('resources\\alliance_tech.png')
       self.alliance_tech_donate= imread('resources\\alliance_tech_donate.png')
       self.alliance_tech_recommend= imread('resources\\alliance_tech_recommend.png')
       self.already_connected= imread('resources\\already_connected.png')
       self.ap_bottle= imread('resources\\ap_bottle.png')
       self.archery_badge= imread('resources\\archery_badge.png')
       self.archery_range_button= imread('resources\\archery_range_button.png')
       self.artefact_shop= imread('resources\\artefact_shop.png')
       self.assist_button= imread('resources\\assist_button.png')
       self.attack_button= imread('resources\\attack_button.png')
       self.back_icon1= imread('resources\\back_icon1.png')
       self.back_icon2= imread('resources\\back_icon2.png')
       self.back_icon3= imread('resources\\back_icon3.png')
       self.back_normal_view= imread('resources\\back_normal_view.png')
       self.barracks_button= imread('resources\\barracks_button.png')
       self.block_icon= imread('resources\\block_icon.png')
       self.bones_icon= imread('resources\\bones_icon.png')
       self.build= imread('resources\\build.png')
       self.builder= imread('resources\\builder.png')
       self.building_info_button= imread('resources\\building_info_button.png')
       self.building_info_button_2= imread('resources\\building_info_button_2.png')
       self.building_speedups= imread('resources\\building_speedups.png')
       self.building_title_left= imread('resources\\building_title_left.png')
       self.button_level= imread('resources\\button_level.png')
       self.buy_arrow= imread('resources\\buy_arrow.png')
       self.cavalry_badge= imread('resources\\cavalry_badge.png')
       self.character_login_confirm= imread('resources\\character_login_confirm.png')
       self.character_start= imread('resources\\character_start.png')
       self.chest_confirm_button= imread('resources\\chest_confirm_button.png')
       self.chest_open_button= imread('resources\\chest_open_button.png')
       self.choose_right= imread('resources\\choose_right.png')
       self.choose_right1= imread('resources\\choose_right1.png')
       self.claim_daily= imread('resources\\claim_daily.png')
       self.claim_quest= imread('resources\\claim_quest.png')
       self.close_refresh_ok= imread('resources\\close_refresh_ok.png')
       self.close_window= imread('resources\\close_window.png')
       self.close_window2= imread('resources\\close_window2.png')
       self.Commander_icon_type_Archer= imread('resources\\Commander_icon_type_Archer.png')
       self.Commander_icon_type_Cavalry= imread('resources\\Commander_icon_type_Cavalry.png')
       self.Commander_icon_type_Infantry= imread('resources\\Commander_icon_type_Infantry.png')
       self.confirm_tavern= imread('resources\\confirm_tavern.png')
       self.cross= imread('resources\\cross.png')
       self.daily_ap_claim= imread('resources\\daily_ap_claim.png')
       self.decreasing_button= imread('resources\\decreasing_button.png')
       self.defeat_mail= imread('resources\\defeat_mail.png')
       self.deploy_march_button= imread('resources\\deploy_march_button.png')
       self.donate_button= imread('resources\\donate_button.png')
       self.download_icon= imread('resources\\download_icon.png')
       self.download_page= imread('resources\\download_page.png')
       self.ebony_icon= imread('resources\\ebony_icon.png')
       self.explore_button= imread('resources\\explore_button.png')
       self.explore_button2= imread('resources\\explore_button2.png')
       self.explore_button_fog= imread('resources\\explore_button_fog.png')
       self.explore_button_scout= imread('resources\\explore_button_scout.png')
       self.food_max= imread('resources\\food_max.png')
       self.food_min= imread('resources\\food_min.png')
       self.forge_1= imread('resources\\forge_1.png')
       self.forge_2= imread('resources\\forge_2.png')
       self.forge_3= imread('resources\\forge_3.png')
       self.forge_4= imread('resources\\forge_4.png')
       self.forge_5= imread('resources\\forge_5.png')
       self.forge_button= imread('resources\\forge_button.png')
       self.forge_icon= imread('resources\\forge_icon.png')
       self.fort= imread('resources\\fort.png')
       self.fort2= imread('resources\\fort2.png')
       self.fort_icon_day_down_left= imread('resources\\fort_icon_day_down_left.png')
       self.fort_icon_day_down_mid= imread('resources\\fort_icon_day_down_mid.png')
       self.fort_icon_day_down_right= imread('resources\\fort_icon_day_down_right.png')
       self.fort_icon_day_mid_left= imread('resources\\fort_icon_day_mid_left.png')
       self.fort_icon_day_mid_mid= imread('resources\\fort_icon_day_mid_mid.png')
       self.fort_icon_day_mid_right= imread('resources\\fort_icon_day_mid_right.png')
       self.fort_icon_day_up_left= imread('resources\\fort_icon_day_up_left.png')
       self.fort_icon_day_up_mid= imread('resources\\fort_icon_day_up_mid.png')
       self.fort_icon_day_up_right= imread('resources\\fort_icon_day_up_right.png')
       self.fort_icon_night_down_left= imread('resources\\fort_icon_night_down_left.png')
       self.fort_icon_night_down_mid= imread('resources\\fort_icon_night_down_mid.png')
       self.fort_icon_night_down_right= imread('resources\\fort_icon_night_down_right.png')
       self.fort_icon_night_mid_left= imread('resources\\fort_icon_night_mid_left.png')
       self.fort_icon_night_mid_mid= imread('resources\\fort_icon_night_mid_mid.png')
       self.fort_icon_night_mid_right= imread('resources\\fort_icon_night_mid_right.png')
       self.fort_icon_night_up_left= imread('resources\\fort_icon_night_up_left.png')
       self.fort_icon_night_up_mid= imread('resources\\fort_icon_night_up_mid.png')
       self.fort_icon_night_up_right= imread('resources\\fort_icon_night_up_right.png')
       self.fort_rally_button1= imread('resources\\fort_rally_button1.png')
       self.fort_rally_button2= imread('resources\\fort_rally_button2.png')
       self.free= imread('resources\\free.png')
       self.gem_icon_day_down_= imread('resources\\gem_icon_day_down_.png')
       self.gem_icon_day_down_left= imread('resources\\gem_icon_day_down_left.png')
       self.gem_icon_day_down_mid= imread('resources\\gem_icon_day_down_mid.png')
       self.gem_icon_day_down_right= imread('resources\\gem_icon_day_down_right.png')
       self.gem_icon_day_mid_left= imread('resources\\gem_icon_day_mid_left.png')
       self.gem_icon_day_mid_mid= imread('resources\\gem_icon_day_mid_mid.png')
       self.gem_icon_day_mid_right= imread('resources\\gem_icon_day_mid_right.png')
       self.gem_icon_day_up_left= imread('resources\\gem_icon_day_up_left.png')
       self.gem_icon_day_up_mid= imread('resources\\gem_icon_day_up_mid.png')
       self.gem_icon_day_up_right= imread('resources\\gem_icon_day_up_right.png')
       self.gem_icon_down_mid= imread('resources\\gem_icon_down_mid.png')
       self.gem_icon_night_down_left= imread('resources\\gem_icon_night_down_left.png')
       self.gem_icon_night_down_mid= imread('resources\\gem_icon_night_down_mid.png')
       self.gem_icon_night_down_right= imread('resources\\gem_icon_night_down_right.png')
       self.gem_icon_night_mid_left= imread('resources\\gem_icon_night_mid_left.png')
       self.gem_icon_night_mid_mid= imread('resources\\gem_icon_night_mid_mid.png')
       self.gem_icon_night_mid_right= imread('resources\\gem_icon_night_mid_right.png')
       self.gem_icon_night_up_left= imread('resources\\gem_icon_night_up_left.png')
       self.gem_icon_night_up_mid= imread('resources\\gem_icon_night_up_mid.png')
       self.gem_icon_night_up_right= imread('resources\\gem_icon_night_up_right.png')
       self.gem_search_button= imread('resources\\gem_search_button.png')
       self.get_more_rss= imread('resources\\get_more_rss.png')
       self.golden_chest= imread('resources\\golden_chest.png')
       self.golden_chest_tiny= imread('resources\\golden_chest_tiny.png')
       self.gold_max= imread('resources\\gold_max.png')
       self.gold_min= imread('resources\\gold_min.png')
       self.great_button= imread('resources\\great_button.png')
       self.green_home_button= imread('resources\\green_home_button.png')
       self.hammer= imread('resources\\hammer.png')
       self.healing_scroll= imread('resources\\healing_scroll.png')
       self.heal_button= imread('resources\\heal_button.png')
       self.heal_icon= imread('resources\\heal_icon.png')
       self.help1= imread('resources\\help1.png')
       self.help2= imread('resources\\help2.png')
       self.help3= imread('resources\\help3.png')
       self.help_alliance= imread('resources\\help_alliance.png')
       self.help_build= imread('resources\\help_build.png')
       self.help_build2= imread('resources\\help_build2.png')
       self.hide_quests= imread('resources\\hide_quests.png')
       self.hire_constructor= imread('resources\\hire_constructor.png')
       self.hire_constructor2= imread('resources\\hire_constructor2.png')
       self.hold_icon= imread('resources\\hold_icon.png')
       self.hold_icon_small= imread('resources\\hold_icon_small.png')
       self.hold_posistion_checked= imread('resources\\hold_posistion_checked.png')
       self.hold_position_unchecked= imread('resources\\hold_position_unchecked.png')
       self.home_button= imread('resources\\home_button.png')
       self.home_button_0= imread('resources\\home_button_0.png')
       self.hut_hammer= imread('resources\\hut_hammer.png')
       self.inbox= imread('resources\\inbox.png')
       self.increasing_button= imread('resources\\increasing_button.png')
       self.infantry_badge= imread('resources\\infantry_badge.png')
       self.investigate_button= imread('resources\\investigate_button.png')
       self.kingdom_buff= imread('resources\\kingdom_buff.png')
       self.leather_icon= imread('resources\\leather_icon.png')
       self.legendary_chest= imread('resources\\legendary_chest.png')
       self.legendary_chest_tiny= imread('resources\\legendary_chest_tiny.png')
       self.lock_button= imread('resources\\lock_button.png')
       self.logged_icon= imread('resources\\logged_icon.png')
       self.mail_exploration_report= imread('resources\\mail_exploration_report.png')
       self.mail_scout_button= imread('resources\\mail_scout_button.png')
       self.map_button= imread('resources\\map_button.png')
       self.map_button_0= imread('resources\\map_button_0.png')
       self.map_icon= imread('resources\\map_icon.png')
       self.maraudeurs_forts_icon= imread('resources\\maraudeurs_forts_icon.png')
       self.maraudeur_icon= imread('resources\\maraudeur_icon.png')
       self.marching_logo= imread('resources\\marching_logo.png')
       self.march_bar= imread('resources\\march_bar.png')
       self.materials_production_button= imread('resources\\materials_production_button.png')
       self.material_chest= imread('resources\\material_chest.png')
       self.menu_button= imread('resources\\menu_button.png')
       self.menu_opened= imread('resources\\menu_opened.png')
       self.merchant_buy_with_food= imread('resources\\merchant_buy_with_food.png')
       self.merchant_buy_with_wood= imread('resources\\merchant_buy_with_wood.png')
       self.merchant_free_btn= imread('resources\\merchant_free_btn.png')
       self.merchant_icon= imread('resources\\merchant_icon.png')
       self.mightiest_gov= imread('resources\\mightiest_gov.png')
       self.minus_button= imread('resources\\minus_button.png')
       self.new_troops_button= imread('resources\\new_troops_button.png')
       self.no= imread('resources\\no.png')
       self.ok= imread('resources\\ok.png')
       self.open_chest= imread('resources\\open_chest.png')
       self.picture2= imread('resources\\picture2.png')
       self.plus_button= imread('resources\\plus_button.png')
       self.popup0= imread('resources\\popup0.png')
       self.popup1= imread('resources\\popup1.png')
       self.preset_1= imread('resources\\preset_1.png')
       self.preset_2= imread('resources\\preset_2.png')
       self.preset_3= imread('resources\\preset_3.png')
       self.preset_4= imread('resources\\preset_4.png')
       self.preset_5= imread('resources\\preset_5.png')
       self.rally_radius= imread('resources\\rally_radius.png')
       self.reconnect= imread('resources\\reconnect.png')
       self.red_icon= imread('resources\\red_icon.png')
       self.red_icon1= imread('resources\\red_icon1.png')
       self.refresh_resolve= imread('resources\\refresh_resolve.png')
       self.resource_gather_button= imread('resources\\resource_gather_button.png')
       self.return_button= imread('resources\\return_button.png')
       self.rokicon= imread('resources\\rokicon.png')
       self.scout_button= imread('resources\\scout_button.png')
       self.scout_button2= imread('resources\\scout_button2.png')
       self.scout_idle_icon= imread('resources\\scout_idle_icon.png')
       self.scout_management= imread('resources\\scout_management.png')
       self.scout_send_button= imread('resources\\scout_send_button.png')
       self.scout_zz_icon= imread('resources\\scout_zz_icon.png')
       self.search_button= imread('resources\\search_button.png')
       self.selected_icon= imread('resources\\selected_icon.png')
       self.selected_save_blue_one= imread('resources\\selected_save_blue_one.png')
       self.send_button_scout= imread('resources\\send_button_scout.png')
       self.siege_badge= imread('resources\\siege_badge.png')
       self.siege_workshop_button= imread('resources\\siege_workshop_button.png')
       self.silver_chest= imread('resources\\silver_chest.png')
       self.silver_chest_tiny= imread('resources\\silver_chest_tiny.png')
       self.speedup_healing= imread('resources\\speedup_healing.png')
       self.speed_up_button= imread('resources\\speed_up_button.png')
       self.stable_button= imread('resources\\stable_button.png')
       self.standby_icon= imread('resources\\standby_icon.png')
       self.stone_icon= imread('resources\\stone_icon.png')
       self.stone_max= imread('resources\\stone_max.png')
       self.stone_min= imread('resources\\stone_min.png')
       self.switch_save= imread('resources\\switch_save.png')
       self.t1_badge= imread('resources\\t1_badge.png')
       self.t2_badge= imread('resources\\t2_badge.png')
       self.t3_badge= imread('resources\\t3_badge.png')
       self.t4_badge= imread('resources\\t4_badge.png')
       self.t5_badge= imread('resources\\t5_badge.png')
       self.tavern_button= imread('resources\\tavern_button.png')
       self.tech= imread('resources\\tech.png')
       self.tech_speedup= imread('resources\\tech_speedup.png')
       self.training_upgrade_button= imread('resources\\training_upgrade_button.png')
       self.train_button= imread('resources\\train_button.png')
       self.troops_march_button= imread('resources\\troops_march_button.png')
       self.troops_march_button2= imread('resources\\troops_march_button2.png')
       self.troop_idle= imread('resources\\troop_idle.png')
       self.troop_walking= imread('resources\\troop_walking.png')
       self.unselect_save_blue_one= imread('resources\\unselect_save_blue_one.png')
       self.upgrade= imread('resources\\upgrade.png')
       self.upgrade_age= imread('resources\\upgrade_age.png')
       self.upgrade_build= imread('resources\\upgrade_build.png')
       self.upgrade_button= imread('resources\\upgrade_button.png')
       self.upgrade_go= imread('resources\\upgrade_go.png')
       self.upgrade_stone= imread('resources\\upgrade_stone.png')
       self.upgrade_stone2= imread('resources\\upgrade_stone2.png')
       self.upgrade_stone3= imread('resources\\upgrade_stone3.png')
       self.use_ap= imread('resources\\use_ap.png')
       self.validate_build= imread('resources\\validate_build.png')
       self.validate_building= imread('resources\\validate_building.png')
       self.verification_button= imread('resources\\verification_button.png')
       self.verification_chest1= imread('resources\\verification_chest1.png')
       self.verification_chest2= imread('resources\\verification_chest2.png')
       self.verification_chest3= imread('resources\\verification_chest3.png')
       self.verification_ok= imread('resources\\verification_ok.png')
       self.verification_verify_title= imread('resources\\verification_verify_title.png')
       self.victory_mail= imread('resources\\victory_mail.png')
       self.window= imread('resources\\window.png')
       self.window_title= imread('resources\\window_title.png')
       self.window_title_mark= imread('resources\\window_title_mark.png')
       self.wood_max= imread('resources\\wood_max.png')
       self.wood_min= imread('resources\\wood_min.png')
       self.yellow_icon= imread('resources\\yellow_icon.png')
       self.yellow_icon1= imread('resources\\yellow_icon1.png')

    def get_file_name(self,file_name):
        if file_name == "academy":
            return self.academy
        if file_name == "academy_tech":
            return self.academy_tech
        if file_name == "alliance_flag1":
            return self.alliance_flag1
        if file_name == "alliance_flag2":
            return self.alliance_flag2
        if file_name == "alliance_gifts_claim_button":
            return self.alliance_gifts_claim_button
        if file_name == "alliance_tech":
            return self.alliance_tech
        if file_name == "alliance_tech_donate":
            return self.alliance_tech_donate
        if file_name == "alliance_tech_recommend":
            return self.alliance_tech_recommend
        if file_name == "already_connected":
            return self.already_connected
        if file_name == "ap_bottle":
            return self.ap_bottle
        if file_name == "archery_badge":
            return self.archery_badge
        if file_name == "archery_range_button":
            return self.archery_range_button
        if file_name == "artefact_shop":
            return self.artefact_shop
        if file_name == "assist_button":
            return self.assist_button
        if file_name == "attack_button":
            return self.attack_button
        if file_name == "back_icon1":
            return self.back_icon1
        if file_name == "back_icon2":
            return self.back_icon2
        if file_name == "back_icon3":
            return self.back_icon3
        if file_name == "back_normal_view":
            return self.back_normal_view
        if file_name == "barracks_button":
            return self.barracks_button
        if file_name == "block_icon":
            return self.block_icon
        if file_name == "bones_icon":
            return self.bones_icon
        if file_name == "build":
            return self.build
        if file_name == "builder":
            return self.builder
        if file_name == "building_info_button":
            return self.building_info_button
        if file_name == "building_info_button_2":
            return self.building_info_button_2
        if file_name == "building_speedups":
            return self.building_speedups
        if file_name == "building_title_left":
            return self.building_title_left
        if file_name == "button_level":
            return self.button_level
        if file_name == "buy_arrow":
            return self.buy_arrow
        if file_name == "cavalry_badge":
            return self.cavalry_badge
        if file_name == "character_login_confirm":
            return self.character_login_confirm
        if file_name == "character_start":
            return self.character_start
        if file_name == "chest_confirm_button":
            return self.chest_confirm_button
        if file_name == "chest_open_button":
            return self.chest_open_button
        if file_name == "choose_right":
            return self.choose_right
        if file_name == "choose_right1":
            return self.choose_right1
        if file_name == "claim_daily":
            return self.claim_daily
        if file_name == "claim_quest":
            return self.claim_quest
        if file_name == "close_refresh_ok":
            return self.close_refresh_ok
        if file_name == "close_window":
            return self.close_window
        if file_name == "close_window2":
            return self.close_window2
        if file_name == "Commander_icon_type_Archer":
            return self.Commander_icon_type_Archer
        if file_name == "Commander_icon_type_Cavalry":
            return self.Commander_icon_type_Cavalry
        if file_name == "Commander_icon_type_Infantry":
            return self.Commander_icon_type_Infantry
        if file_name == "confirm_tavern":
            return self.confirm_tavern
        if file_name == "cross":
            return self.cross
        if file_name == "daily_ap_claim":
            return self.daily_ap_claim
        if file_name == "decreasing_button":
            return self.decreasing_button
        if file_name == "defeat_mail":
            return self.defeat_mail
        if file_name == "deploy_march_button":
            return self.deploy_march_button
        if file_name == "donate_button":
            return self.donate_button
        if file_name == "download_icon":
            return self.download_icon
        if file_name == "download_page":
            return self.download_page
        if file_name == "ebony_icon":
            return self.ebony_icon
        if file_name == "explore_button":
            return self.explore_button
        if file_name == "explore_button2":
            return self.explore_button2
        if file_name == "explore_button_fog":
            return self.explore_button_fog
        if file_name == "explore_button_scout":
            return self.explore_button_scout
        if file_name == "food_max":
            return self.food_max
        if file_name == "food_min":
            return self.food_min
        if file_name == "forge_1":
            return self.forge_1
        if file_name == "forge_2":
            return self.forge_2
        if file_name == "forge_3":
            return self.forge_3
        if file_name == "forge_4":
            return self.forge_4
        if file_name == "forge_5":
            return self.forge_5
        if file_name == "forge_button":
            return self.forge_button
        if file_name == "forge_icon":
            return self.forge_icon
        if file_name == "fort":
            return self.fort
        if file_name == "fort2":
            return self.fort2
        if file_name == "fort_icon_day_down_left":
            return self.fort_icon_day_down_left
        if file_name == "fort_icon_day_down_mid":
            return self.fort_icon_day_down_mid
        if file_name == "fort_icon_day_down_right":
            return self.fort_icon_day_down_right
        if file_name == "fort_icon_day_mid_left":
            return self.fort_icon_day_mid_left
        if file_name == "fort_icon_day_mid_mid":
            return self.fort_icon_day_mid_mid
        if file_name == "fort_icon_day_mid_right":
            return self.fort_icon_day_mid_right
        if file_name == "fort_icon_day_up_left":
            return self.fort_icon_day_up_left
        if file_name == "fort_icon_day_up_mid":
            return self.fort_icon_day_up_mid
        if file_name == "fort_icon_day_up_right":
            return self.fort_icon_day_up_right
        if file_name == "fort_icon_night_down_left":
            return self.fort_icon_night_down_left
        if file_name == "fort_icon_night_down_mid":
            return self.fort_icon_night_down_mid
        if file_name == "fort_icon_night_down_right":
            return self.fort_icon_night_down_right
        if file_name == "fort_icon_night_mid_left":
            return self.fort_icon_night_mid_left
        if file_name == "fort_icon_night_mid_mid":
            return self.fort_icon_night_mid_mid
        if file_name == "fort_icon_night_mid_right":
            return self.fort_icon_night_mid_right
        if file_name == "fort_icon_night_up_left":
            return self.fort_icon_night_up_left
        if file_name == "fort_icon_night_up_mid":
            return self.fort_icon_night_up_mid
        if file_name == "fort_icon_night_up_right":
            return self.fort_icon_night_up_right
        if file_name == "fort_rally_button1":
            return self.fort_rally_button1
        if file_name == "fort_rally_button2":
            return self.fort_rally_button2
        if file_name == "free":
            return self.free
        if file_name == "gem_icon_day_down_":
            return self.gem_icon_day_down_
        if file_name == "gem_icon_day_down_left":
            return self.gem_icon_day_down_left
        if file_name == "gem_icon_day_down_mid":
            return self.gem_icon_day_down_mid
        if file_name == "gem_icon_day_down_right":
            return self.gem_icon_day_down_right
        if file_name == "gem_icon_day_mid_left":
            return self.gem_icon_day_mid_left
        if file_name == "gem_icon_day_mid_mid":
            return self.gem_icon_day_mid_mid
        if file_name == "gem_icon_day_mid_right":
            return self.gem_icon_day_mid_right
        if file_name == "gem_icon_day_up_left":
            return self.gem_icon_day_up_left
        if file_name == "gem_icon_day_up_mid":
            return self.gem_icon_day_up_mid
        if file_name == "gem_icon_day_up_right":
            return self.gem_icon_day_up_right
        if file_name == "gem_icon_down_mid":
            return self.gem_icon_down_mid
        if file_name == "gem_icon_night_down_left":
            return self.gem_icon_night_down_left
        if file_name == "gem_icon_night_down_mid":
            return self.gem_icon_night_down_mid
        if file_name == "gem_icon_night_down_right":
            return self.gem_icon_night_down_right
        if file_name == "gem_icon_night_mid_left":
            return self.gem_icon_night_mid_left
        if file_name == "gem_icon_night_mid_mid":
            return self.gem_icon_night_mid_mid
        if file_name == "gem_icon_night_mid_right":
            return self.gem_icon_night_mid_right
        if file_name == "gem_icon_night_up_left":
            return self.gem_icon_night_up_left
        if file_name == "gem_icon_night_up_mid":
            return self.gem_icon_night_up_mid
        if file_name == "gem_icon_night_up_right":
            return self.gem_icon_night_up_right
        if file_name == "gem_search_button":
            return self.gem_search_button
        if file_name == "get_more_rss":
            return self.get_more_rss
        if file_name == "golden_chest":
            return self.golden_chest
        if file_name == "golden_chest_tiny":
            return self.golden_chest_tiny
        if file_name == "gold_max":
            return self.gold_max
        if file_name == "gold_min":
            return self.gold_min
        if file_name == "great_button":
            return self.great_button
        if file_name == "green_home_button":
            return self.green_home_button
        if file_name == "hammer":
            return self.hammer
        if file_name == "healing_scroll":
            return self.healing_scroll
        if file_name == "heal_button":
            return self.heal_button
        if file_name == "heal_icon":
            return self.heal_icon
        if file_name == "help1":
            return self.help1
        if file_name == "help2":
            return self.help2
        if file_name == "help3":
            return self.help3
        if file_name == "help_alliance":
            return self.help_alliance
        if file_name == "help_build":
            return self.help_build
        if file_name == "help_build2":
            return self.help_build2
        if file_name == "hide_quests":
            return self.hide_quests
        if file_name == "hire_constructor":
            return self.hire_constructor
        if file_name == "hire_constructor2":
            return self.hire_constructor2
        if file_name == "hold_icon":
            return self.hold_icon
        if file_name == "hold_icon_small":
            return self.hold_icon_small
        if file_name == "hold_posistion_checked":
            return self.hold_posistion_checked
        if file_name == "hold_position_unchecked":
            return self.hold_position_unchecked
        if file_name == "home_button":
            return self.home_button
        if file_name == "home_button_0":
            return self.home_button_0
        if file_name == "hut_hammer":
            return self.hut_hammer
        if file_name == "inbox":
            return self.inbox
        if file_name == "increasing_button":
            return self.increasing_button
        if file_name == "infantry_badge":
            return self.infantry_badge
        if file_name == "investigate_button":
            return self.investigate_button
        if file_name == "kingdom_buff":
            return self.kingdom_buff
        if file_name == "leather_icon":
            return self.leather_icon
        if file_name == "legendary_chest":
            return self.legendary_chest
        if file_name == "legendary_chest_tiny":
            return self.legendary_chest_tiny
        if file_name == "lock_button":
            return self.lock_button
        if file_name == "logged_icon":
            return self.logged_icon
        if file_name == "mail_exploration_report":
            return self.mail_exploration_report
        if file_name == "mail_scout_button":
            return self.mail_scout_button
        if file_name == "map_button":
            return self.map_button
        if file_name == "map_button_0":
            return self.map_button_0
        if file_name == "map_icon":
            return self.map_icon
        if file_name == "maraudeurs_forts_icon":
            return self.maraudeurs_forts_icon
        if file_name == "maraudeur_icon":
            return self.maraudeur_icon
        if file_name == "marching_logo":
            return self.marching_logo
        if file_name == "march_bar":
            return self.march_bar
        if file_name == "materials_production_button":
            return self.materials_production_button
        if file_name == "material_chest":
            return self.material_chest
        if file_name == "menu_button":
            return self.menu_button
        if file_name == "menu_opened":
            return self.menu_opened
        if file_name == "merchant_buy_with_food":
            return self.merchant_buy_with_food
        if file_name == "merchant_buy_with_wood":
            return self.merchant_buy_with_wood
        if file_name == "merchant_free_btn":
            return self.merchant_free_btn
        if file_name == "merchant_icon":
            return self.merchant_icon
        if file_name == "mightiest_gov":
            return self.mightiest_gov
        if file_name == "minus_button":
            return self.minus_button
        if file_name == "new_troops_button":
            return self.new_troops_button
        if file_name == "no":
            return self.no
        if file_name == "ok":
            return self.ok
        if file_name == "open_chest":
            return self.open_chest
        if file_name == "picture2":
            return self.picture2
        if file_name == "plus_button":
            return self.plus_button
        if file_name == "popup0":
            return self.popup0
        if file_name == "popup1":
            return self.popup1
        if file_name == "preset_1":
            return self.preset_1
        if file_name == "preset_2":
            return self.preset_2
        if file_name == "preset_3":
            return self.preset_3
        if file_name == "preset_4":
            return self.preset_4
        if file_name == "preset_5":
            return self.preset_5
        if file_name == "rally_radius":
            return self.rally_radius
        if file_name == "reconnect":
            return self.reconnect
        if file_name == "red_icon":
            return self.red_icon
        if file_name == "red_icon1":
            return self.red_icon1
        if file_name == "refresh_resolve":
            return self.refresh_resolve
        if file_name == "resource_gather_button":
            return self.resource_gather_button
        if file_name == "return_button":
            return self.return_button
        if file_name == "rokicon":
            return self.rokicon
        if file_name == "scout_button":
            return self.scout_button
        if file_name == "scout_button2":
            return self.scout_button2
        if file_name == "scout_idle_icon":
            return self.scout_idle_icon
        if file_name == "scout_management":
            return self.scout_management
        if file_name == "scout_send_button":
            return self.scout_send_button
        if file_name == "scout_zz_icon":
            return self.scout_zz_icon
        if file_name == "search_button":
            return self.search_button
        if file_name == "selected_icon":
            return self.selected_icon
        if file_name == "selected_save_blue_one":
            return self.selected_save_blue_one
        if file_name == "send_button_scout":
            return self.send_button_scout
        if file_name == "siege_badge":
            return self.siege_badge
        if file_name == "siege_workshop_button":
            return self.siege_workshop_button
        if file_name == "silver_chest":
            return self.silver_chest
        if file_name == "silver_chest_tiny":
            return self.silver_chest_tiny
        if file_name == "speedup_healing":
            return self.speedup_healing
        if file_name == "speed_up_button":
            return self.speed_up_button
        if file_name == "stable_button":
            return self.stable_button
        if file_name == "standby_icon":
            return self.standby_icon
        if file_name == "stone_icon":
            return self.stone_icon
        if file_name == "stone_max":
            return self.stone_max
        if file_name == "stone_min":
            return self.stone_min
        if file_name == "switch_save":
            return self.switch_save
        if file_name == "t1_badge":
            return self.t1_badge
        if file_name == "t2_badge":
            return self.t2_badge
        if file_name == "t3_badge":
            return self.t3_badge
        if file_name == "t4_badge":
            return self.t4_badge
        if file_name == "t5_badge":
            return self.t5_badge
        if file_name == "tavern_button":
            return self.tavern_button
        if file_name == "tech":
            return self.tech
        if file_name == "tech_speedup":
            return self.tech_speedup
        if file_name == "training_upgrade_button":
            return self.training_upgrade_button
        if file_name == "train_button":
            return self.train_button
        if file_name == "troops_march_button":
            return self.troops_march_button
        if file_name == "troops_march_button2":
            return self.troops_march_button2
        if file_name == "troop_idle":
            return self.troop_idle
        if file_name == "troop_walking":
            return self.troop_walking
        if file_name == "unselect_save_blue_one":
            return self.unselect_save_blue_one
        if file_name == "upgrade":
            return self.upgrade
        if file_name == "upgrade_age":
            return self.upgrade_age
        if file_name == "upgrade_build":
            return self.upgrade_build
        if file_name == "upgrade_button":
            return self.upgrade_button
        if file_name == "upgrade_go":
            return self.upgrade_go
        if file_name == "upgrade_stone":
            return self.upgrade_stone
        if file_name == "upgrade_stone2":
            return self.upgrade_stone2
        if file_name == "upgrade_stone3":
            return self.upgrade_stone3
        if file_name == "use_ap":
            return self.use_ap
        if file_name == "validate_build":
            return self.validate_build
        if file_name == "validate_building":
            return self.validate_building
        if file_name == "verification_button":
            return self.verification_button
        if file_name == "verification_chest1":
            return self.verification_chest1
        if file_name == "verification_chest2":
            return self.verification_chest2
        if file_name == "verification_chest3":
            return self.verification_chest3
        if file_name == "verification_ok":
            return self.verification_ok
        if file_name == "verification_verify_title":
            return self.verification_verify_title
        if file_name == "victory_mail":
            return self.victory_mail
        if file_name == "window":
            return self.window
        if file_name == "window_title":
            return self.window_title
        if file_name == "window_title_mark":
            return self.window_title_mark
        if file_name == "wood_max":
            return self.wood_max
        if file_name == "wood_min":
            return self.wood_min
        if file_name == "yellow_icon":
            return self.yellow_icon
        if file_name == "yellow_icon1":
            return self.yellow_icon1
        else:
            return imread('resources\\' + file_name + '.png')
