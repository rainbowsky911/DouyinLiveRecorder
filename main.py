# coding=utf-8
import sys



import dylr.core.app as app


def main():
    # 自动识别以命令行还是GUI形式运行
    # 服务器部署时，强制使用CLI模式
    # if len(sys.argv) > 1 and sys.argv[1] == '--cli':
    #     run_cli()
    # elif sys.stdin and sys.stdin.isatty():
    #     run_cli()
    # else:
        run_gui()


def run_cli():
    app.init(False)


def run_gui():
    app.init(True)
    ...


if __name__ == '__main__':
    main()
