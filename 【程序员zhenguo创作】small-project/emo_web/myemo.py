import re
import emoji


def search(target, inner=True):
    if not target:
        return ''
    # 第一次求表情
    emm = emoji.emojize(target)
    if emm != target:
        if inner:
            return [(emm, target)]
        else:
            return emm
    # 第二次
    words = re.split(r'_+|\W+', target)
    em_list, ks = list(), set()
    for word in words:
        if len(word) == 0:
            continue
        patten = re.compile(r'%s' % word, flags=re.IGNORECASE)

        for emm in emoji.UNICODE_EMOJI_ENGLISH:
            em_std = emoji.UNICODE_EMOJI_ENGLISH[emm]
            if patten.search(em_std) and em_std not in ks:
                found = emoji.emojize(em_std)
                em_list.append((found, em_std))
                ks.add(em_std)
    if inner:
        return sorted(em_list, key=lambda x: len(x[0]))
    else:
        ems = sorted(em_list, key=lambda x: len(x[0]))
        return [em[0] for em in ems]


def search_all():
    return [(k, v) for k, v in emoji.UNICODE_EMOJI_ENGLISH.items()]


if __name__ == "__main__":
    print(search('heart'))
