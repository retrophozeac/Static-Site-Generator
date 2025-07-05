from textnode import *
def main():
    text1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text1)

if __name__ == "__main__":
    main()