import argparse
import csv
import os
import re
import sys
import time
from datetime import datetime
from time import sleep

import clipboard
from PIL import ImageEnhance, ImageOps, Image

from tasks.Task import Task
from utils.functions import get_class

RANKING_TAP_POS_X = 760
# ランキングタップ位置（Y軸、[1位,2位,3位,4位-998位,999位,1000位]）
RANKING_TAP_POS_Y = (280, 384, 485, 613, 713, 813)
# 撃破詳細タップ位置
KILL_DETAIL_TAP_POS = (1117, 352)
# 詳細情報タップ位置
PLAYER_DETAIL_TAP_POS = (386, 667)
ID_CROP_RANGE = (735, 236, 880, 268)

aapo = None
template_dir_path = None
dir_path = None
img_dir_path = None
log_dir_path = None

# 同盟タグの切り抜き範囲
ALLIANCE_CROP_RANGE = (644, 365, 763, 396)

# IDの切り抜き範囲

# 撃破数の切り抜き範囲
# (
#   (T1撃破数範囲),
#   (T2撃破数範囲),
#   ...
# )
KILL_CROP_RANGES = (
    (863, 468, 1068, 494),
    (863, 512, 1068, 538),
    (863, 556, 1068, 582),
    (863, 600, 1068, 626),
    (863, 645, 1068, 671),
)

# 撃破ポイントの切り抜き範囲
# (
#   (T1撃破数範囲),
#   (T2撃破数範囲),
#   ...
# )
KILL_POINT_CROP_RANGES = (
    (1211, 468, 1415, 494),
    (1211, 512, 1415, 538),
    (1211, 556, 1415, 582),
    (1211, 600, 1415, 626),
    (1211, 645, 1415, 671),
)

# 撃破ポイント係数
# (T1, T2, T3, T4, T5)
KILL_POINT_COEFFICIENTS = (0.2, 2, 4, 10, 20)

# 遠隔ポイントの切り抜き範囲
RANGED_POINT_CROP_RANGE = (1118, 744, 1415, 775)

# 戦力の切り抜き範囲
POWER_CROP_RANGE = (809, 141, 1009, 173)

# 過去最大戦力の切り抜き範囲
HIGHEST_POWER_CROP_RANGE = (1103, 266, 1303, 296)

# 戦死数の切り抜き範囲
DEAD_CROP_RANGE = (1103, 450, 1303, 480)

# 資源援助数の切り抜き範囲
RSS_CROP_RANGE = (1053, 680, 1303, 710)

tool = None

current_rank: int = 0


class KingdomRanking(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)

    def task_name(self):
        return "KingdomRanking"

    @get_class
    def run(self):
        # ランキングタップ位置（X軸）
        global adb, template_dir_path, dir_path, img_dir_path, log_dir_path

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-d", "--dir", type=str, default=datetime.now().strftime("%Y-%m-%d")
        )
        parser.add_argument("-s", "--start-rank", type=int, default=1)
        parser.add_argument("-e", "--end-rank", type=int, default=300)
        args = parser.parse_args()

        print(f"\n===== Scanning from {args.start_rank} to {args.end_rank}. =====\n")

        template_dir_path = ""
        dir_path = "./"
        img_dir_path = dir_path + "screenshots/"
        log_dir_path = dir_path + "logs/autocap/"

        os.makedirs(log_dir_path, exist_ok=True)

        start_rank: int = args.start_rank - 1
        end_rank: int = args.end_rank

        self.auto_capture(start_rank, end_rank)

        print("\n===== Done! =====")

    def auto_capture(self, start: int, end: int):
        global current_rank
        self.writeCsv([
            'Rank',
            'ID',
            'Name',
            'Alliance',
            'Power',
            'Hpower',
            'Kills_1',
            'Kills_2',
            'Kills_3',
            'Kills_4',
            'Kills_5',
            'Ranged',
            'Dead',
            'Rss'
        ]
        )
        for i in range(start, end):
            current_rank = i + 1

            print(f"\n===== Currently scanning player rank : {current_rank}. =====\n")

            # 総督情報表示
            if current_rank <= 3:
                self.adb.click(RANKING_TAP_POS_X, RANKING_TAP_POS_Y[i])
            elif current_rank == 999:
                self.adb.click(RANKING_TAP_POS_X, RANKING_TAP_POS_Y[4])
            elif current_rank == 1000:
                self.adb.click(RANKING_TAP_POS_X, RANKING_TAP_POS_Y[5])
            else:
                self.adb.click(RANKING_TAP_POS_X, RANKING_TAP_POS_Y[3])
            sleep(0.5)

            try:
                self.checkImg(template_dir_path + "player")
            except TimeoutError:
                self.err(f"An error occurred when scanning {current_rank}")
                if self.find_img(template_dir_path + "ranking"):
                    self.adb.swipe_arg(
                        RANKING_TAP_POS_X,
                        RANKING_TAP_POS_Y[3],
                        RANKING_TAP_POS_X,
                        RANKING_TAP_POS_Y[3] - 100,
                        1000,
                    )
                    continue
                else:
                    self.err(f"An error occurred when scanning {current_rank}, the bot has to stop.")
                    sys.exit(1)

            # 撃破詳細表示・キャプチャ
            self.click(KILL_DETAIL_TAP_POS[0], KILL_DETAIL_TAP_POS[1])
            sleep(0.5)

            try:
                self.checkImg(template_dir_path + "kill")
            except TimeoutError:
                self.err(f"An error occurred when scanning {current_rank}. Returning to the Ranking Screen")
                self.returnToRankingScreen()
                continue

            self.adb.save_screen(img_dir_path + str(current_rank) + "a")

            # 詳細情報表示・キャプチャ
            self.click(PLAYER_DETAIL_TAP_POS[0], PLAYER_DETAIL_TAP_POS[1])
            sleep(0.5)

            self.adb.save_screen(img_dir_path + str(current_rank) + "b")

            # 総督名保存
            with open(
                    img_dir_path + "names.tsv",
                    "a+",
                    encoding="utf_8",
                    newline=""
            ) as fh:
                fh.seek(0)
                co = self.find_img(template_dir_path + "copy")
                self.click(co[0], co[1])
                sleep(0.1)
                names = list(csv.reader(fh, delimiter="\t"))
                current_name = clipboard.paste()
                names.append([str(current_rank), current_name])
                fh.truncate(0)
                fh.seek(0)
                csv.writer(fh, delimiter="\t").writerows(
                    sorted(names, key=lambda x: int(x[0]))
                )

            # ランキングまで戻る
            self.returnToRankingScreen()
            self.writeCsv(self.ocr_images(str(current_rank), current_name))

    def checkImg(self, img_path: str):
        timer = 0
        while True:
            print(self.find_img(img_path))
            if self.find_img(img_path):
                break
            elif timer >= 4:
                raise TimeoutError
            else:
                timer += 1
                sleep(1)

    def returnToRankingScreen(self):
        timer = 0
        while True:
            if self.find_img(template_dir_path + "ranking"):
                break
            elif timer >= 4:
                self.err(f"Unable to return to the ranking screen, current rank was : {current_rank}")
                sys.exit(1)
            else:
                co = self.find_img(template_dir_path + "close")
                self.click(co[0], co[1])
                timer += 1
                sleep(1)

    def err(self, message: str, fzelp):
        print(message)
        with open(
                log_dir_path + "error.log", "a", encoding="utf_8"
        ) as fh:
            fh.write(message + "\n")
        self.adb.save_screen(log_dir_path + str(current_rank) + "")

    def mainocr(self):
        startTime = time.time()

        global tool, dir_path, img_dir_path, log_dir_path

        parser = argparse.ArgumentParser()
        parser.add_argument("dir", type=str)
        parser.add_argument("-j", "--jobs", type=int, default=-2)
        args = parser.parse_args()

        data = []

        os.makedirs(log_dir_path, exist_ok=True)

        with open(dir_path + args.dir + ".tsv", "w", encoding="utf_8", newline="") as fh:
            data = sorted(data, key=lambda x: int(x[0]))
            data.insert(
                0,
                (
                    "Rank",
                    "ID",
                    "Name",
                    "Alliance",
                    "Power",
                    "Highest Power",
                    "T1 Kills",
                    "T2 Kills",
                    "T3 Kills",
                    "T4 Kills",
                    "T5 Kills",
                    "Ranged Points",
                    "Dead",
                    "RSS",
                ),
            )
            csv.writer(fh, delimiter="\t").writerows(data)

        endTime = time.time()
        print(f"\n処理時間：{endTime - startTime}")

    def ocr_images(self, rank: str, name: str):
        img_a = Image.open(img_dir_path + rank + "a.png")
        if img_a.mode == "RGBA":
            img_a = img_a.convert("RGB")

        img_b = Image.open(img_dir_path + rank + "b.png")
        if img_b.mode == "RGBA":
            img_b = img_b.convert("RGB")

        # ID
        id_img = self.correct_image(img_a, ID_CROP_RANGE, threshold=50, contrast=5, brightness=2)
        id = self.ocr_image(id_img, whitelist="0123456789)")
        id = re.sub("\)$", "", id)
        if id == "":
            self.err(
                f"{rank}th - {name}: Failed to read 'ID'. -> {rank}-id",
                [(f"{rank}-id", id_img)],
            )

        # 同盟タグ
        alliance_img = self.correct_image(
            img_a, ALLIANCE_CROP_RANGE, scale=5, contrast=1.3, brightness=2
        )
        alliance = self.ocr_image(
            alliance_img,
            whitelist=f"[]0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        )
        alliance = re.match(r"^\[(.{3,4})\]", alliance)
        if alliance is None:
            alliance = ""
        else:
            alliance = alliance.group(1)

        # 撃破
        kills = []
        for i, (
                kill_crop_range,
                kill_point_crop_range,
                kill_point_coefficient,
        ) in enumerate(
            zip(KILL_CROP_RANGES, KILL_POINT_CROP_RANGES, KILL_POINT_COEFFICIENTS)
        ):
            kill_img = self.correct_image(
                img_a,
                kill_crop_range,
                threshold=50,
                invert=False,
                brightness=1.2,
                contrast=1.2,
            )
            kill = self.ocr_image(kill_img)
            kill_p_img = self.correct_image(
                img_a,
                kill_point_crop_range,
                threshold=50,
                invert=False,
                brightness=1.2,
                contrast=1.2,
            )
            kill_p = self.ocr_image(kill_p_img)

            kill = kill.replace(",", "")
            kill_p = kill_p.replace(",", "")

            kill_img_file_name = rank + "-t" + str(i + 1) + "-kill"
            kill_p_img_file_name = rank + "-t" + str(i + 1) + "-kill-point"

            if kill == "":
                self.err(
                    f"{rank}th - {name}: Failed to read 'T{i + 1} Kill Count'. -> {kill_img_file_name}, {kill_p_img_file_name}",
                    [(kill_img_file_name, kill_img), (kill_p_img_file_name, kill_p_img)],
                )
            elif abs(int(kill) * kill_point_coefficient - int(kill_p)) > 1:
                self.err(
                    f"{rank}th - {name}: There may be a failure in reading 'T{i + 1} Kill Count' accurately. OCR result: Kill Count: '{kill}', Kill Points: '{kill_p}'. -> {kill_img_file_name}, {kill_p_img_file_name}",
                    [(kill_img_file_name, kill_img), (kill_p_img_file_name, kill_p_img)],
                )

            kills.append(kill)

        # 遠隔ポイント
        ranged_img = self.correct_image(
            img_a,
            RANGED_POINT_CROP_RANGE,
            threshold=50,
            invert=False,
            brightness=1.2,
            contrast=1.2,
        )
        ranged = self.ocr_image(ranged_img)
        ranged = ranged.replace(",", "")
        if ranged == "":
            self.err(
                f"{rank}th - {name}: Failed to read 'Ranged Points'. -> {rank}-ranged",
                [(f"{rank}-ranged", ranged_img)],
            )
        # 戦力
        power_img = self.correct_image(
            img_b, POWER_CROP_RANGE, threshold=50, brightness=2, contrast=1.2
        )
        power = self.ocr_image(power_img)
        power = power.replace(",", "")
        if power == "":
            self.err(
                f"{rank}th - {name}: Failed to read 'Power'. -> {rank}-power",
                [(f"{rank}-power", power_img)],
            )

        # 過去最大戦力
        hpower_img = self.correct_image(
            img_b, HIGHEST_POWER_CROP_RANGE, brightness=1.3, contrast=1.8
        )
        hpower = self.ocr_image(hpower_img)
        hpower = hpower.replace(",", "")
        if hpower == "":
            self.err(
                f"{rank}th - {name}: Failed to read 'Highest Power'. -> {rank}-hpower",
                [(f"{rank}-dead", hpower_img)],
            )

        # 戦力チェック
        if power != "" and hpower != "" and int(power) > int(hpower):
            self.err(
                f"{rank}th - {name}: There may be a failure in reading 'Power' or 'Highest Power' accurately. OCR results: Power: '{power}', Highest Power: '{hpower}'. -> {rank}-power, {rank}-hpower",
                [(f"{rank}-power", power_img), (f"{rank}-hpower", hpower_img)],
            )

        # 戦死
        dead_img = self.correct_image(img_b, DEAD_CROP_RANGE, brightness=1.3, contrast=1.8)
        dead = self.ocr_image(dead_img)
        dead = dead.replace(",", "")
        if dead == "":
            self.err(
                f"{rank}th - {name}: Failed to read 'Death Count'. -> {rank}-dead",
                [(f"{rank}-dead", dead_img)],
            )
        # 資源援助
        rss_img = self.correct_image(img_b, RSS_CROP_RANGE, brightness=1.3, contrast=1.8)
        rss = self.ocr_image(rss_img)
        rss = rss.replace(",", "")
        if rss == "":
            self.err(
                f"{rank}th - {name}: Failed to read 'Resource Assistance Count'. -> {rank}-rss",
                [(f"{rank}-rss", rss_img)],
            )

        print(
            f"{rank} {id} {name} {alliance} {power} {hpower} {kills[0]} {kills[1]} {kills[2]} {kills[3]} {kills[4]} {ranged} {dead} {rss}"
        )

        return [
            rank,
            id,
            name,
            alliance,
            power,
            hpower,
            kills[0],
            kills[1],
            kills[2],
            kills[3],
            kills[4],
            ranged,
            dead,
            rss,
        ]

    def writeCsv(self, array):
        import csv

        with open('rankings.csv', mode='a+', encoding='utf-8', newline='') as ranking_file:
            rankings = csv.writer(ranking_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            print(array)
            rankings.writerow(array)

    def correct_image(self,
                      img: Image.Image,
                      crop_range: tuple,
                      threshold: int = 0,
                      threshold_max: int = -1,
                      invert: bool = True,
                      scale: float = 1,
                      contrast: float = 1,
                      brightness: float = 1,
                      ) -> Image.Image:
        tmp = img.crop(crop_range)
        tmp = ImageOps.invert(tmp) if invert else tmp
        tmp = tmp.convert("L")
        tmp = (
            tmp.resize((round(tmp.width * scale), round(tmp.height * scale)))
            if scale != 1
            else tmp
        )
        tmp = ImageEnhance.Contrast(tmp).enhance(contrast) if contrast != 1 else tmp
        tmp = ImageEnhance.Brightness(tmp).enhance(brightness) if brightness != 1 else tmp
        if threshold == 0:
            pass
        elif threshold_max == -1:
            tmp = tmp.point(lambda x: 0 if x < threshold else x)
        else:
            tmp = tmp.point(lambda x: 0 if x < threshold else threshold_max)
        return tmp

    def ocr_image(self, img: Image, whitelist: str = "0123456789,") -> str:
        return self.extract_text(img, allowlist=whitelist)
