
import re
import subprocess
import tabulate

detectors = ["SHITOMASI", "HARRIS", "BRISK", "ORB", "FAST", "AKAZE", "SIFT"]
descriptors = ["BRISK", "BRIEF", "ORB", "FREAK", "AKAZE", "SIFT"]
all_stats = []

def mp7_f(all_stats):
    print("MP7:")
    processed = []
    mp7 = []
    header = ['DETECTOR']
    for i in range(1, 11):
        header.append(f"img{i}")

    for stat in all_stats:
        if stat['detector'] in processed:
            continue
        processed.append(stat['detector'])
        entry = [stat['detector']]
        for img in stat['img_stats']:
            entry.append(img['nodes'])
        mp7.append(entry)
    print(tabulate.tabulate(mp7, header))

def mp8_f(all_stats):
    print("MP8:")
    processed = []
    mp8 = []
    header = ['DETECTOR', 'DESCRIPTOR']
    for i in range(1, 11):
        header.append(f"img{i}")

    for stat in all_stats:
        entry = [stat['detector'], stat['descriptor']]
        for img in stat['img_stats']:
            entry.append(img['matches'])
        mp8.append(entry)

    print(tabulate.tabulate(mp8, header))

def mp9_f(all_stats):
    tmp = sorted(all_stats, key = lambda i: i['det_avg'])

    found = []
    mp9 = []
    print("TOP 3 detectors:")
    for stat in tmp:
        if len(found) == 3:
            break;
        if stat['detector'] in found:
            continue
        found.append(stat['detector'])
        mp9.append([stat['detector'], stat['det_avg']])
    print(tabulate.tabulate(mp9, ['DETECTOR', 'AVG TIME']))
    print()

    tmp = sorted(all_stats, key = lambda i: i['desc_avg'])
    found = []
    mp9 = []
    print("TOP 3 extractors:")
    for stat in tmp:
        if len(found) == 3:
            break;
        if stat['descriptor'] in found:
            continue
        found.append(stat['descriptor'])
        mp9.append([stat['descriptor'], stat['desc_avg']])
    print(tabulate.tabulate(mp9, ['DESCRIPTOR', 'AVG TIME']))
    print()

    tmp = sorted(all_stats, key = lambda i: i['total_avg'])
    found = []
    mp9 = []
    print("TOP 3 detector and extractor combination:")
    for stat in tmp:
        if len(found) == 3:
            break;
        if (stat['detector'], stat['descriptor']) in found:
            continue
        found.append((stat['detector'], stat['descriptor']))
        mp9.append([stat['detector'], stat['descriptor'], stat['total_avg']])
    print(tabulate.tabulate(mp9, ['DETECTOR','DESCRIPTOR', 'AVG TIME']))
    print()

# MAIN

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
                desc_stats_str = out[i+4]
                match_stats_str = "- -"

                if len(img_stats) > 0:
                    match_stats_str = out[i+6]

                out.pop(i)

                tmp = re.split(r'\s', det_stats_str)
                detected_nodes = tmp[3]
                det_time = tmp[6]
                desc_time = re.split(r'\s', desc_stats_str)[4]
                matched_nodes = re.split(r'\s', match_stats_str)[1]

                stat = {}
                stat["img"] = img_num
                stat["detector"] = det
                stat["descriptor"] = desc
                stat["matcher"] = "MAT_BF"
                stat["selector"] = sel
                stat["nodes"] = detected_nodes
                stat["matches"] = matched_nodes
                stat["det_time"] = det_time
                stat["desc_time"] = desc_time
                img_stats.append(stat)

                img_num += 1

            stats_table = []
            detector_avg = 0.0
            extractor_avg = 0.0
            for stat in img_stats:
                '''
                stats_table.append([stat["img"],
                                    stat["detector"],
                                    stat["descriptor"],
                                    stat["matcher"],
                                    stat["selector"],
                                    stat["nodes"],
                                    stat["matches"],
                                    stat["det_time"],
                                    stat["desc_time"],
                                     ])
                '''
                detector_avg += float(stat["det_time"])
                extractor_avg += float(stat["desc_time"])
            total_avg = detector_avg + extractor_avg
            #print(tabulate.tabulate(stats_table,
            #                        ['IMG #', 'DETECTOR', 'DESCRIPTOR', 'MATCHER', 'SELECTOR', 'DET NODES', 'MATCHES', 'DETECTION TIME', 'EXTRACTION TIME']))
            #print()

            if sel == "SEL_KNN":
                detector_avg = detector_avg / len(img_stats)
                extractor_avg = extractor_avg / len(img_stats)
                total_avg = total_avg / len(img_stats)
                stat = {}
                stat["img_stats"] = img_stats
                stat["detector"] = det
                stat["descriptor"] = desc
                stat["matcher"] = "MAT_BF"
                stat["selector"] = sel
                stat["det_avg"] = detector_avg
                stat["desc_avg"] = extractor_avg
                stat["total_avg"] = total_avg

                all_stats.append(stat)


mp7_f(all_stats)
mp8_f(all_stats)
mp9_f(all_stats)
