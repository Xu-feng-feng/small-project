from myemo import search


def emo(key):
    key = key.strip()
    return search(key, False)


if __name__ == "__main__":
    print("Python" + emo(":thumbs_up:"))
    print("我%sPython" % emo(':smiling_face_with_hearts:'))

    print("Python能做很多事情%s\n如下打印6个方向键%s" % (
        emo(":smiling_face_with_sunglasses:"), emo("	:sunflower:")))
    print("%s%s%s" % (emo(":up-left_arrow:"),
                      emo(":up_arrow:"), emo(":up-right_arrow:")))
    print("%s%s%s" % (emo(":down-left_arrow:"),
                      emo(":down_arrow:"), emo(":down-right_arrow:")))

    with open("emo.md", 'w') as f:
        content = ("Python{}，我{}Python\nPython能做很多事情\n"
                   "如下打印6个方向键：\n{}{}{}\n{}{}{}".format(
            emo(":thumbs_up:"), emo(':smiling_face_with_hearts:'),
            emo(":up-left_arrow:"), emo(":up_arrow:"), emo(":up-right_arrow:"),
            emo(":down-left_arrow:"), emo(":down_arrow:"), emo(":down-right_arrow:")
        ))
        f.write(content)
