
import re
import subprocess
import tabulate

detectors = ["SHITOMASI", "HARRIS", "BRISK", "ORB", "FAST", "AKAZE", "SIFT"]
descriptors = ["BRISK", "BRIEF", "ORB", "FREAK", "AKAZE", "SIFT"]


for det in detectors:
    for desc in descriptors:
        for sel in ["SEL_NN", "SEL_KNN"]:
            ps = subprocess.run(['../build/2D_feature_tracking', det, desc, 'MAT_BF', sel],
                                capture_output=True, text=True)

            if ps.returncode != 0:
                print(f"{det} + {desc} + {sel} combo is invalid")
                continue

            out = ps.stdout
            out = out.split('\n')

            img_stats = []
            img_num = 1
            ENTRY_POINT = '#1 : LOAD IMAGE INTO BUFFER done'
            while ENTRY_POINT in out:
                i = out.index(ENTRY_POINT)
                det_stats_str = out[i+1]
                desc_stats_str = out[i+5]

                out.pop(i)

                tmp = re.split(r'\s', det_stats_str)
                detected_nodes = tmp[3]
                det_time = tmp[6]
                desc_time = re.split(r'\s', desc_stats_str)[4]
                stat = {}
                stat["img"] = img_num
                stat["detector"] = det
                stat["descriptor"] = desc
                stat["matcher"] = "MAT_BF"
                stat["selector"] = sel
                stat["nodes"] = detected_nodes
                stat["det_time"] = det_time
                stat["desc_time"] = desc_time
                img_stats.append(stat)

                img_num += 1

            stats_table = []
            for stat in img_stats:
                stats_table.append([stat["img"],
                                    stat["detector"],
                                    stat["descriptor"],
                                    stat["matcher"],
                                    stat["selector"],
                                    stat["nodes"],
                                    stat["det_time"],
                                    stat["desc_time"],
                                     ])

            print(tabulate.tabulate(stats_table, ['IMG #', 'DETECTOR', 'DESCRIPTOR', 'MATCHER', 'SELECTOR', '# of NODES', 'DETECTION TIME', 'EXTRACTION TIME']))
            print()



