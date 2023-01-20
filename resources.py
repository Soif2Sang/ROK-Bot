from cv2 import cvtColor, imread, matchTemplate, minMaxLoc, COLOR_BGR2RGB, TM_CCOEFF_NORMED, imdecode,         IMREAD_COLOR, COLOR_BGR2HSV, inRange
academy= imread('resources\\academy.png')
academy_tech= imread('resources\\academy_tech.png')
alliance_flag1= imread('resources\\alliance_flag1.png')
alliance_flag2= imread('resources\\alliance_flag2.png')
alliance_gifts_claim_button= imread('resources\\alliance_gifts_claim_button.png')
alliance_tech= imread('resources\\alliance_tech.png')
alliance_tech_donate= imread('resources\\alliance_tech_donate.png')
alliance_tech_recommend= imread('resources\\alliance_tech_recommend.png')
already_connected= imread('resources\\already_connected.png')
ap_bottle= imread('resources\\ap_bottle.png')
archery_range_button= imread('resources\\archery_range_button.png')
attack_button= imread('resources\\attack_button.png')
back_icon1= imread('resources\\back_icon1.png')
back_icon2= imread('resources\\back_icon2.png')
back_icon3= imread('resources\\back_icon3.png')
back_normal_view= imread('resources\\back_normal_view.png')
barracks_button= imread('resources\\barracks_button.png')
block_icon= imread('resources\\block_icon.png')
bones_icon= imread('resources\\bones_icon.png')
build= imread('resources\\build.png')
builder= imread('resources\\builder.png')
building_info_button= imread('resources\\building_info_button.png')
building_info_button_2= imread('resources\\building_info_button_2.png')
building_speedups= imread('resources\\building_speedups.png')
building_title_left= imread('resources\\building_title_left.png')
button_level= imread('resources\\button_level.png')
buy_arrow= imread('resources\\buy_arrow.png')
character_login_confirm= imread('resources\\character_login_confirm.png')
character_start= imread('resources\\character_start.png')
chest_confirm_button= imread('resources\\chest_confirm_button.png')
chest_open_button= imread('resources\\chest_open_button.png')
choose_right= imread('resources\\choose_right.png')
choose_right1= imread('resources\\choose_right1.png')
claim_daily= imread('resources\\claim_daily.png')
claim_quest= imread('resources\\claim_quest.png')
close_refresh_ok= imread('resources\\close_refresh_ok.png')
close_window= imread('resources\\close_window.png')
Commander_icon_type_Archer= imread('resources\\Commander_icon_type_Archer.png')
Commander_icon_type_Cavalry= imread('resources\\Commander_icon_type_Cavalry.png')
Commander_icon_type_Infantry= imread('resources\\Commander_icon_type_Infantry.png')
confirm_tavern= imread('resources\\confirm_tavern.png')
cross= imread('resources\\cross.png')
daily_ap_claim= imread('resources\\daily_ap_claim.png')
decreasing_button= imread('resources\\decreasing_button.png')
defeat_mail= imread('resources\\defeat_mail.png')
deploy_march_button= imread('resources\\deploy_march_button.png')
donate_button= imread('resources\\donate_button.png')
download_icon= imread('resources\\download_icon.png')
download_page= imread('resources\\download_page.png')
ebony_icon= imread('resources\\ebony_icon.png')
explore_button= imread('resources\\explore_button.png')
explore_button2= imread('resources\\explore_button2.png')
explore_button_fog= imread('resources\\explore_button_fog.png')
explore_button_scout= imread('resources\\explore_button_scout.png')
food_max= imread('resources\\food_max.png')
food_min= imread('resources\\food_min.png')
forge_1= imread('resources\\forge_1.png')
forge_2= imread('resources\\forge_2.png')
forge_3= imread('resources\\forge_3.png')
forge_4= imread('resources\\forge_4.png')
forge_5= imread('resources\\forge_5.png')
forge_button= imread('resources\\forge_button.png')
forge_icon= imread('resources\\forge_icon.png')
fort= imread('resources\\fort.png')
fort2= imread('resources\\fort2.png')
fort_icon_day_down_left= imread('resources\\fort_icon_day_down_left.png')
fort_icon_day_down_mid= imread('resources\\fort_icon_day_down_mid.png')
fort_icon_day_down_right= imread('resources\\fort_icon_day_down_right.png')
fort_icon_day_mid_left= imread('resources\\fort_icon_day_mid_left.png')
fort_icon_day_mid_mid= imread('resources\\fort_icon_day_mid_mid.png')
fort_icon_day_mid_right= imread('resources\\fort_icon_day_mid_right.png')
fort_icon_day_up_left= imread('resources\\fort_icon_day_up_left.png')
fort_icon_day_up_mid= imread('resources\\fort_icon_day_up_mid.png')
fort_icon_day_up_right= imread('resources\\fort_icon_day_up_right.png')
fort_icon_night_down_left= imread('resources\\fort_icon_night_down_left.png')
fort_icon_night_down_mid= imread('resources\\fort_icon_night_down_mid.png')
fort_icon_night_down_right= imread('resources\\fort_icon_night_down_right.png')
fort_icon_night_mid_left= imread('resources\\fort_icon_night_mid_left.png')
fort_icon_night_mid_mid= imread('resources\\fort_icon_night_mid_mid.png')
fort_icon_night_mid_right= imread('resources\\fort_icon_night_mid_right.png')
fort_icon_night_up_left= imread('resources\\fort_icon_night_up_left.png')
fort_icon_night_up_mid= imread('resources\\fort_icon_night_up_mid.png')
fort_icon_night_up_right= imread('resources\\fort_icon_night_up_right.png')
fort_rally_button1= imread('resources\\fort_rally_button1.png')
fort_rally_button2= imread('resources\\fort_rally_button2.png')
free= imread('resources\\free.png')
gem_icon_day_down_= imread('resources\\gem_icon_day_down_.png')
gem_icon_day_down_left= imread('resources\\gem_icon_day_down_left.png')
gem_icon_day_down_mid= imread('resources\\gem_icon_day_down_mid.png')
gem_icon_day_down_right= imread('resources\\gem_icon_day_down_right.png')
gem_icon_day_mid_left= imread('resources\\gem_icon_day_mid_left.png')
gem_icon_day_mid_mid= imread('resources\\gem_icon_day_mid_mid.png')
gem_icon_day_mid_right= imread('resources\\gem_icon_day_mid_right.png')
gem_icon_day_up_left= imread('resources\\gem_icon_day_up_left.png')
gem_icon_day_up_mid= imread('resources\\gem_icon_day_up_mid.png')
gem_icon_day_up_right= imread('resources\\gem_icon_day_up_right.png')
gem_icon_down_mid= imread('resources\\gem_icon_down_mid.png')
gem_icon_night_down_left= imread('resources\\gem_icon_night_down_left.png')
gem_icon_night_down_mid= imread('resources\\gem_icon_night_down_mid.png')
gem_icon_night_down_right= imread('resources\\gem_icon_night_down_right.png')
gem_icon_night_mid_left= imread('resources\\gem_icon_night_mid_left.png')
gem_icon_night_mid_mid= imread('resources\\gem_icon_night_mid_mid.png')
gem_icon_night_mid_right= imread('resources\\gem_icon_night_mid_right.png')
gem_icon_night_up_left= imread('resources\\gem_icon_night_up_left.png')
gem_icon_night_up_mid= imread('resources\\gem_icon_night_up_mid.png')
gem_icon_night_up_right= imread('resources\\gem_icon_night_up_right.png')
gem_search_button= imread('resources\\gem_search_button.png')
get_more_rss= imread('resources\\get_more_rss.png')
golden_chest= imread('resources\\golden_chest.png')
gold_max= imread('resources\\gold_max.png')
gold_min= imread('resources\\gold_min.png')
great_button= imread('resources\\great_button.png')
green_home_button= imread('resources\\green_home_button.png')
hammer= imread('resources\\hammer.png')
healing_scroll= imread('resources\\healing_scroll.png')
heal_button= imread('resources\\heal_button.png')
heal_icon= imread('resources\\heal_icon.png')
help= imread('resources\\help.png')
help_alliance= imread('resources\\help_alliance.png')
help_build= imread('resources\\help_build.png')
help_build2= imread('resources\\help_build2.png')
hide_quests= imread('resources\\hide_quests.png')
hire_constructor= imread('resources\\hire_constructor.png')
hold_icon= imread('resources\\hold_icon.png')
hold_icon_small= imread('resources\\hold_icon_small.png')
hold_posistion_checked= imread('resources\\hold_posistion_checked.png')
hold_position_unchecked= imread('resources\\hold_position_unchecked.png')
home_button= imread('resources\\home_button.png')
home_button_0= imread('resources\\home_button_0.png')
hut_hammer= imread('resources\\hut_hammer.png')
inbox= imread('resources\\inbox.png')
increasing_button= imread('resources\\increasing_button.png')
investigate_button= imread('resources\\investigate_button.png')
kingdom_buff= imread('resources\\kingdom_buff.png')
leather_icon= imread('resources\\leather_icon.png')
legendary_chest= imread('resources\\legendary_chest.png')
lock_button= imread('resources\\lock_button.png')
logged_icon= imread('resources\\logged_icon.png')
mail_exploration_report= imread('resources\\mail_exploration_report.png')
mail_scout_button= imread('resources\\mail_scout_button.png')
map_button= imread('resources\\map_button.png')
map_button_0= imread('resources\\map_button_0.png')
map_icon= imread('resources\\map_icon.png')
maraudeurs_forts_icon= imread('resources\\maraudeurs_forts_icon.png')
maraudeur_icon= imread('resources\\maraudeur_icon.png')
marching_logo= imread('resources\\marching_logo.png')
march_bar= imread('resources\\march_bar.png')
materials_production_button= imread('resources\\materials_production_button.png')
material_chest= imread('resources\\material_chest.png')
menu_button= imread('resources\\menu_button.png')
menu_opened= imread('resources\\menu_opened.png')
merchant_buy_with_food= imread('resources\\merchant_buy_with_food.png')
merchant_buy_with_wood= imread('resources\\merchant_buy_with_wood.png')
merchant_free_btn= imread('resources\\merchant_free_btn.png')
merchant_icon= imread('resources\\merchant_icon.png')
mightiest_gov= imread('resources\\mightiest_gov.png')
minus_button= imread('resources\\minus_button.png')
new_troops_button= imread('resources\\new_troops_button.png')
no= imread('resources\\no.png')
ok= imread('resources\\ok.png')
open_chest= imread('resources\\open_chest.png')
picture2= imread('resources\\picture2.png')
plus_button= imread('resources\\plus_button.png')
popup0= imread('resources\\popup0.png')
popup1= imread('resources\\popup1.png')
preset_1= imread('resources\\preset_1.png')
preset_2= imread('resources\\preset_2.png')
preset_3= imread('resources\\preset_3.png')
preset_4= imread('resources\\preset_4.png')
preset_5= imread('resources\\preset_5.png')
rally_radius= imread('resources\\rally_radius.png')
reconnect= imread('resources\\reconnect.png')
red_icon= imread('resources\\red_icon.png')
red_icon1= imread('resources\\red_icon1.png')
refresh_resolve= imread('resources\\refresh_resolve.png')
resource_gather_button= imread('resources\\resource_gather_button.png')
return_button= imread('resources\\return_button.png')
rokicon= imread('resources\\rokicon.png')
scout_button= imread('resources\\scout_button.png')
scout_button2= imread('resources\\scout_button2.png')
scout_idle_icon= imread('resources\\scout_idle_icon.png')
scout_management= imread('resources\\scout_management.png')
scout_send_button= imread('resources\\scout_send_button.png')
scout_zz_icon= imread('resources\\scout_zz_icon.png')
search_button= imread('resources\\search_button.png')
selected_icon= imread('resources\\selected_icon.png')
selected_save_blue_one= imread('resources\\selected_save_blue_one.png')
send_button_scout= imread('resources\\send_button_scout.png')
siege_workshop_button= imread('resources\\siege_workshop_button.png')
silver_chest= imread('resources\\silver_chest.png')
speedup_healing= imread('resources\\speedup_healing.png')
speed_up_button= imread('resources\\speed_up_button.png')
stable_button= imread('resources\\stable_button.png')
standby_icon= imread('resources\\standby_icon.png')
stone_icon= imread('resources\\stone_icon.png')
stone_max= imread('resources\\stone_max.png')
stone_min= imread('resources\\stone_min.png')
switch_save= imread('resources\\switch_save.png')
t1_badge= imread('resources\\t1_badge.png')
t2_badge= imread('resources\\t2_badge.png')
t3_badge= imread('resources\\t3_badge.png')
t4_badge= imread('resources\\t4_badge.png')
t5_badge= imread('resources\\t5_badge.png')
tavern_button= imread('resources\\tavern_button.png')
tech= imread('resources\\tech.png')
tech_speedup= imread('resources\\tech_speedup.png')
training_upgrade_button= imread('resources\\training_upgrade_button.png')
train_button= imread('resources\\train_button.png')
troops_march_button= imread('resources\\troops_march_button.png')
troops_march_button2= imread('resources\\troops_march_button2.png')
troop_idle= imread('resources\\troop_idle.png')
troop_walking= imread('resources\\troop_walking.png')
unselect_save_blue_one= imread('resources\\unselect_save_blue_one.png')
upgrade= imread('resources\\upgrade.png')
upgrade_age= imread('resources\\upgrade_age.png')
upgrade_build= imread('resources\\upgrade_build.png')
upgrade_button= imread('resources\\upgrade_button.png')
upgrade_go= imread('resources\\upgrade_go.png')
upgrade_stone= imread('resources\\upgrade_stone.png')
upgrade_stone2= imread('resources\\upgrade_stone2.png')
use_ap= imread('resources\\use_ap.png')
validate_build= imread('resources\\validate_build.png')
validate_building= imread('resources\\validate_building.png')
verification_button= imread('resources\\verification_button.png')
verification_chest1= imread('resources\\verification_chest1.png')
verification_chest2= imread('resources\\verification_chest2.png')
verification_chest3= imread('resources\\verification_chest3.png')
verification_ok= imread('resources\\verification_ok.png')
verification_verify_title= imread('resources\\verification_verify_title.png')
victory_mail= imread('resources\\victory_mail.png')
window= imread('resources\\window.png')
window_title= imread('resources\\window_title.png')
window_title_mark= imread('resources\\window_title_mark.png')
wood_max= imread('resources\\wood_max.png')
wood_min= imread('resources\\wood_min.png')
yellow_icon= imread('resources\\yellow_icon.png')
yellow_icon1= imread('resources\\yellow_icon1.png')

def get_file_name(file_name):
    if file_name == "academy":
        return academy
    if file_name == "academy_tech":
        return academy_tech
    if file_name == "alliance_flag1":
        return alliance_flag1
    if file_name == "alliance_flag2":
        return alliance_flag2
    if file_name == "alliance_gifts_claim_button":
        return alliance_gifts_claim_button
    if file_name == "alliance_tech":
        return alliance_tech
    if file_name == "alliance_tech_donate":
        return alliance_tech_donate
    if file_name == "alliance_tech_recommend":
        return alliance_tech_recommend
    if file_name == "already_connected":
        return already_connected
    if file_name == "ap_bottle":
        return ap_bottle
    if file_name == "archery_range_button":
        return archery_range_button
    if file_name == "attack_button":
        return attack_button
    if file_name == "back_icon1":
        return back_icon1
    if file_name == "back_icon2":
        return back_icon2
    if file_name == "back_icon3":
        return back_icon3
    if file_name == "back_normal_view":
        return back_normal_view
    if file_name == "barracks_button":
        return barracks_button
    if file_name == "block_icon":
        return block_icon
    if file_name == "bones_icon":
        return bones_icon
    if file_name == "build":
        return build
    if file_name == "builder":
        return builder
    if file_name == "building_info_button":
        return building_info_button
    if file_name == "building_info_button_2":
        return building_info_button_2
    if file_name == "building_speedups":
        return building_speedups
    if file_name == "building_title_left":
        return building_title_left
    if file_name == "button_level":
        return button_level
    if file_name == "buy_arrow":
        return buy_arrow
    if file_name == "character_login_confirm":
        return character_login_confirm
    if file_name == "character_start":
        return character_start
    if file_name == "chest_confirm_button":
        return chest_confirm_button
    if file_name == "chest_open_button":
        return chest_open_button
    if file_name == "choose_right":
        return choose_right
    if file_name == "choose_right1":
        return choose_right1
    if file_name == "claim_daily":
        return claim_daily
    if file_name == "claim_quest":
        return claim_quest
    if file_name == "close_refresh_ok":
        return close_refresh_ok
    if file_name == "close_window":
        return close_window
    if file_name == "Commander_icon_type_Archer":
        return Commander_icon_type_Archer
    if file_name == "Commander_icon_type_Cavalry":
        return Commander_icon_type_Cavalry
    if file_name == "Commander_icon_type_Infantry":
        return Commander_icon_type_Infantry
    if file_name == "confirm_tavern":
        return confirm_tavern
    if file_name == "cross":
        return cross
    if file_name == "daily_ap_claim":
        return daily_ap_claim
    if file_name == "decreasing_button":
        return decreasing_button
    if file_name == "defeat_mail":
        return defeat_mail
    if file_name == "deploy_march_button":
        return deploy_march_button
    if file_name == "donate_button":
        return donate_button
    if file_name == "download_icon":
        return download_icon
    if file_name == "download_page":
        return download_page
    if file_name == "ebony_icon":
        return ebony_icon
    if file_name == "explore_button":
        return explore_button
    if file_name == "explore_button2":
        return explore_button2
    if file_name == "explore_button_fog":
        return explore_button_fog
    if file_name == "explore_button_scout":
        return explore_button_scout
    if file_name == "food_max":
        return food_max
    if file_name == "food_min":
        return food_min
    if file_name == "forge_1":
        return forge_1
    if file_name == "forge_2":
        return forge_2
    if file_name == "forge_3":
        return forge_3
    if file_name == "forge_4":
        return forge_4
    if file_name == "forge_5":
        return forge_5
    if file_name == "forge_button":
        return forge_button
    if file_name == "forge_icon":
        return forge_icon
    if file_name == "fort":
        return fort
    if file_name == "fort2":
        return fort2
    if file_name == "fort_icon_day_down_left":
        return fort_icon_day_down_left
    if file_name == "fort_icon_day_down_mid":
        return fort_icon_day_down_mid
    if file_name == "fort_icon_day_down_right":
        return fort_icon_day_down_right
    if file_name == "fort_icon_day_mid_left":
        return fort_icon_day_mid_left
    if file_name == "fort_icon_day_mid_mid":
        return fort_icon_day_mid_mid
    if file_name == "fort_icon_day_mid_right":
        return fort_icon_day_mid_right
    if file_name == "fort_icon_day_up_left":
        return fort_icon_day_up_left
    if file_name == "fort_icon_day_up_mid":
        return fort_icon_day_up_mid
    if file_name == "fort_icon_day_up_right":
        return fort_icon_day_up_right
    if file_name == "fort_icon_night_down_left":
        return fort_icon_night_down_left
    if file_name == "fort_icon_night_down_mid":
        return fort_icon_night_down_mid
    if file_name == "fort_icon_night_down_right":
        return fort_icon_night_down_right
    if file_name == "fort_icon_night_mid_left":
        return fort_icon_night_mid_left
    if file_name == "fort_icon_night_mid_mid":
        return fort_icon_night_mid_mid
    if file_name == "fort_icon_night_mid_right":
        return fort_icon_night_mid_right
    if file_name == "fort_icon_night_up_left":
        return fort_icon_night_up_left
    if file_name == "fort_icon_night_up_mid":
        return fort_icon_night_up_mid
    if file_name == "fort_icon_night_up_right":
        return fort_icon_night_up_right
    if file_name == "fort_rally_button1":
        return fort_rally_button1
    if file_name == "fort_rally_button2":
        return fort_rally_button2
    if file_name == "free":
        return free
    if file_name == "gem_icon_day_down_":
        return gem_icon_day_down_
    if file_name == "gem_icon_day_down_left":
        return gem_icon_day_down_left
    if file_name == "gem_icon_day_down_mid":
        return gem_icon_day_down_mid
    if file_name == "gem_icon_day_down_right":
        return gem_icon_day_down_right
    if file_name == "gem_icon_day_mid_left":
        return gem_icon_day_mid_left
    if file_name == "gem_icon_day_mid_mid":
        return gem_icon_day_mid_mid
    if file_name == "gem_icon_day_mid_right":
        return gem_icon_day_mid_right
    if file_name == "gem_icon_day_up_left":
        return gem_icon_day_up_left
    if file_name == "gem_icon_day_up_mid":
        return gem_icon_day_up_mid
    if file_name == "gem_icon_day_up_right":
        return gem_icon_day_up_right
    if file_name == "gem_icon_down_mid":
        return gem_icon_down_mid
    if file_name == "gem_icon_night_down_left":
        return gem_icon_night_down_left
    if file_name == "gem_icon_night_down_mid":
        return gem_icon_night_down_mid
    if file_name == "gem_icon_night_down_right":
        return gem_icon_night_down_right
    if file_name == "gem_icon_night_mid_left":
        return gem_icon_night_mid_left
    if file_name == "gem_icon_night_mid_mid":
        return gem_icon_night_mid_mid
    if file_name == "gem_icon_night_mid_right":
        return gem_icon_night_mid_right
    if file_name == "gem_icon_night_up_left":
        return gem_icon_night_up_left
    if file_name == "gem_icon_night_up_mid":
        return gem_icon_night_up_mid
    if file_name == "gem_icon_night_up_right":
        return gem_icon_night_up_right
    if file_name == "gem_search_button":
        return gem_search_button
    if file_name == "get_more_rss":
        return get_more_rss
    if file_name == "golden_chest":
        return golden_chest
    if file_name == "gold_max":
        return gold_max
    if file_name == "gold_min":
        return gold_min
    if file_name == "great_button":
        return great_button
    if file_name == "green_home_button":
        return green_home_button
    if file_name == "hammer":
        return hammer
    if file_name == "healing_scroll":
        return healing_scroll
    if file_name == "heal_button":
        return heal_button
    if file_name == "heal_icon":
        return heal_icon
    if file_name == "help":
        return help
    if file_name == "help_alliance":
        return help_alliance
    if file_name == "help_build":
        return help_build
    if file_name == "help_build2":
        return help_build2
    if file_name == "hide_quests":
        return hide_quests
    if file_name == "hire_constructor":
        return hire_constructor
    if file_name == "hold_icon":
        return hold_icon
    if file_name == "hold_icon_small":
        return hold_icon_small
    if file_name == "hold_posistion_checked":
        return hold_posistion_checked
    if file_name == "hold_position_unchecked":
        return hold_position_unchecked
    if file_name == "home_button":
        return home_button
    if file_name == "home_button_0":
        return home_button_0
    if file_name == "hut_hammer":
        return hut_hammer
    if file_name == "inbox":
        return inbox
    if file_name == "increasing_button":
        return increasing_button
    if file_name == "investigate_button":
        return investigate_button
    if file_name == "kingdom_buff":
        return kingdom_buff
    if file_name == "leather_icon":
        return leather_icon
    if file_name == "legendary_chest":
        return legendary_chest
    if file_name == "lock_button":
        return lock_button
    if file_name == "logged_icon":
        return logged_icon
    if file_name == "mail_exploration_report":
        return mail_exploration_report
    if file_name == "mail_scout_button":
        return mail_scout_button
    if file_name == "map_button":
        return map_button
    if file_name == "map_button_0":
        return map_button_0
    if file_name == "map_icon":
        return map_icon
    if file_name == "maraudeurs_forts_icon":
        return maraudeurs_forts_icon
    if file_name == "maraudeur_icon":
        return maraudeur_icon
    if file_name == "marching_logo":
        return marching_logo
    if file_name == "march_bar":
        return march_bar
    if file_name == "materials_production_button":
        return materials_production_button
    if file_name == "material_chest":
        return material_chest
    if file_name == "menu_button":
        return menu_button
    if file_name == "menu_opened":
        return menu_opened
    if file_name == "merchant_buy_with_food":
        return merchant_buy_with_food
    if file_name == "merchant_buy_with_wood":
        return merchant_buy_with_wood
    if file_name == "merchant_free_btn":
        return merchant_free_btn
    if file_name == "merchant_icon":
        return merchant_icon
    if file_name == "mightiest_gov":
        return mightiest_gov
    if file_name == "minus_button":
        return minus_button
    if file_name == "new_troops_button":
        return new_troops_button
    if file_name == "no":
        return no
    if file_name == "ok":
        return ok
    if file_name == "open_chest":
        return open_chest
    if file_name == "picture2":
        return picture2
    if file_name == "plus_button":
        return plus_button
    if file_name == "popup0":
        return popup0
    if file_name == "popup1":
        return popup1
    if file_name == "preset_1":
        return preset_1
    if file_name == "preset_2":
        return preset_2
    if file_name == "preset_3":
        return preset_3
    if file_name == "preset_4":
        return preset_4
    if file_name == "preset_5":
        return preset_5
    if file_name == "rally_radius":
        return rally_radius
    if file_name == "reconnect":
        return reconnect
    if file_name == "red_icon":
        return red_icon
    if file_name == "red_icon1":
        return red_icon1
    if file_name == "refresh_resolve":
        return refresh_resolve
    if file_name == "resource_gather_button":
        return resource_gather_button
    if file_name == "return_button":
        return return_button
    if file_name == "rokicon":
        return rokicon
    if file_name == "scout_button":
        return scout_button
    if file_name == "scout_button2":
        return scout_button2
    if file_name == "scout_idle_icon":
        return scout_idle_icon
    if file_name == "scout_management":
        return scout_management
    if file_name == "scout_send_button":
        return scout_send_button
    if file_name == "scout_zz_icon":
        return scout_zz_icon
    if file_name == "search_button":
        return search_button
    if file_name == "selected_icon":
        return selected_icon
    if file_name == "selected_save_blue_one":
        return selected_save_blue_one
    if file_name == "send_button_scout":
        return send_button_scout
    if file_name == "siege_workshop_button":
        return siege_workshop_button
    if file_name == "silver_chest":
        return silver_chest
    if file_name == "speedup_healing":
        return speedup_healing
    if file_name == "speed_up_button":
        return speed_up_button
    if file_name == "stable_button":
        return stable_button
    if file_name == "standby_icon":
        return standby_icon
    if file_name == "stone_icon":
        return stone_icon
    if file_name == "stone_max":
        return stone_max
    if file_name == "stone_min":
        return stone_min
    if file_name == "switch_save":
        return switch_save
    if file_name == "t1_badge":
        return t1_badge
    if file_name == "t2_badge":
        return t2_badge
    if file_name == "t3_badge":
        return t3_badge
    if file_name == "t4_badge":
        return t4_badge
    if file_name == "t5_badge":
        return t5_badge
    if file_name == "tavern_button":
        return tavern_button
    if file_name == "tech":
        return tech
    if file_name == "tech_speedup":
        return tech_speedup
    if file_name == "training_upgrade_button":
        return training_upgrade_button
    if file_name == "train_button":
        return train_button
    if file_name == "troops_march_button":
        return troops_march_button
    if file_name == "troops_march_button2":
        return troops_march_button2
    if file_name == "troop_idle":
        return troop_idle
    if file_name == "troop_walking":
        return troop_walking
    if file_name == "unselect_save_blue_one":
        return unselect_save_blue_one
    if file_name == "upgrade":
        return upgrade
    if file_name == "upgrade_age":
        return upgrade_age
    if file_name == "upgrade_build":
        return upgrade_build
    if file_name == "upgrade_button":
        return upgrade_button
    if file_name == "upgrade_go":
        return upgrade_go
    if file_name == "upgrade_stone":
        return upgrade_stone
    if file_name == "upgrade_stone2":
        return upgrade_stone2
    if file_name == "use_ap":
        return use_ap
    if file_name == "validate_build":
        return validate_build
    if file_name == "validate_building":
        return validate_building
    if file_name == "verification_button":
        return verification_button
    if file_name == "verification_chest1":
        return verification_chest1
    if file_name == "verification_chest2":
        return verification_chest2
    if file_name == "verification_chest3":
        return verification_chest3
    if file_name == "verification_ok":
        return verification_ok
    if file_name == "verification_verify_title":
        return verification_verify_title
    if file_name == "victory_mail":
        return victory_mail
    if file_name == "window":
        return window
    if file_name == "window_title":
        return window_title
    if file_name == "window_title_mark":
        return window_title_mark
    if file_name == "wood_max":
        return wood_max
    if file_name == "wood_min":
        return wood_min
    if file_name == "yellow_icon":
        return yellow_icon
    if file_name == "yellow_icon1":
        return yellow_icon1
    else:
        return imread('resources\\' + file_name + '.png')
