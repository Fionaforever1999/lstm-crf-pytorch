from utils import *

def load_data():
    data = []
    if KEEP_IDX:
        cti = load_tkn_to_idx(sys.argv[1] + ".char_to_idx")
        wti = load_tkn_to_idx(sys.argv[1] + ".word_to_idx")
        tti = load_tkn_to_idx(sys.argv[1] + ".tag_to_idx")
    else:
        cti = {PAD: PAD_IDX, SOS: SOS_IDX, EOS: EOS_IDX, UNK: UNK_IDX}
        wti = {PAD: PAD_IDX, SOS: SOS_IDX, EOS: EOS_IDX, UNK: UNK_IDX}
        tti = {PAD: PAD_IDX, SOS: SOS_IDX, EOS: EOS_IDX}
        if FORMAT == "char+iob":
            tti["B"] = len(tti)
            tti["I"] = len(tti)
    fo = open(sys.argv[1])
    for line in fo:
        line = line.strip()
        tokens = line.split(" ")
        x = []
        y = []
        for w in tokens:
            if FORMAT == "word+tag":
                w, tag = re.split("/(?=[^/]+$)", w)
                w = normalize(w)
            if not KEEP_IDX:
                for c in w:
                    if c not in cti:
                        cti[c] = len(cti)
                if w not in wti:
                    wti[w] = len(wti)
                if FORMAT == "word+tag":
                    if tag not in tti:
                        tti[tag] = len(tti)
            if FORMAT == "char+iob":
                x.extend(["%d:%d" % (cti[c], cti[c]) for c in w])
                y.extend([str(tti["B"])] + [str(tti["I"])] * (len(w) - 1))
            if FORMAT == "word+tag":
                x.append("+".join(str(cti[c]) for c in w) + ":%d" % wti[w])
                y.append(str(tti[tag]))
        print(line)
        print(x)
        print(y)
        data.append(x + y)
    fo.close()
    data.sort(key = lambda x: -len(x))
    return data, cti, wti, tti

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s training_data" % sys.argv[0])
    data, cti, wti, tti = load_data()
    save_data(sys.argv[1] + ".csv", data)
    if not KEEP_IDX:
        save_tkn_to_idx(sys.argv[1] + ".char_to_idx", cti)
        save_tkn_to_idx(sys.argv[1] + ".word_to_idx", wti)
        save_tkn_to_idx(sys.argv[1] + ".tag_to_idx", tti)
