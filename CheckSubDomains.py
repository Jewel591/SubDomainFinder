# -*- coding: UTF-8 -*-
import subprocess
import os
import sys
import re
import argparse
import time

parser = argparse.ArgumentParser()
parser.description="CheckSubDomains 是一个整合了 subDomainsBrute 和 Sublist3r 两者结果的子域名收集工具，并添加了批量收集域名的功能"

f_domains = open("./input/domains.txt",'r')
countall=len(open("./input/domains.txt",'r').readlines())
countnow = 1
print '\033[1;31;8m[+] 检测 Python 2.7 环境\033[0m'
pwd = os.path.abspath(".") #获取当前路径
try:
    os.chdir(pwd+"/subDomainsBrute") #切换到 subDomainsBrute 目录并调用执行 subDomainsBrute.py
except:
    print '调用 subDomainsBrute.py 失败...'
    sys.exit(0)
print '\033[1;31;8m[+] 调用 subDomainsBrute.py 检测...\033[0m'
subprocess.call("pwd", shell=True)

for domain in f_domains.readlines():
    mycommand = "python2.7 "+pwd+"/subDomainsBrute/subDomainsBrute.py -i -t 300 --full -o "+pwd+"/output/"+domain.replace("\n","")+".txt"+" "+domain
    print '\033[1;31;8m[+] subDomainsBrute 正在检测域名:\033[0m',domain.replace("\n",""),'[',countnow,'/',countall,']'
    # print '[+] 执行命令： ', mycommand
    countnow+=1
    p=subprocess.Popen(mycommand, shell=True)
    p.wait()

#### 下面开始调用 Sublist3r ####

print '\033[1;31;8m[+] subDomainsBrute 检测完成，结果存放在./output/目录下\033[0m'

countnow = 1
try:
    os.chdir(pwd+"/Sublist3r") #切换到 subDomainsBrute 目录并调用执行 subDomainsBrute.py
except:
    print '调用 Sublist3r.py 失败...'
    sys.exit(0)
print '\033[1;31;8m[+] 调用 Sublist3r.py 检测...(Sublist3r 检测速度较慢请耐心等待，打开 VPN/SSR/V2RAY 全局代理可提高检测速度并使结果更全面)\033[0m'
subprocess.call("pwd", shell=True)

for domain in open("../input/domains.txt",'r').readlines():
    mycommand = "python2.7 "+pwd+"/Sublist3r/sublist3r.py -v -e baidu,dnsdumpster,yahoo,bing,ask,netcraft,virustotal,passivedns,threatcrowd,ssl,google -t 100 -o "+pwd+"/Sublist3r/output/"+domain.replace("\n","")+".txt2"+" -d "+domain
    print '\033[1;31;8m[+] Sublist3r 正在检测域名:\033[0m',domain.replace("\n",""),'[',countnow,'/',countall,']'
    # print '[+] 执行命令： ', mycommand
    countnow+=1
    p=subprocess.Popen(mycommand, shell=True)
    p.wait()

# 去重、整合、格式化
print "Sublist3r 检测完成，正在合并结果..."
print '\033[1;31;8m[+] Sublist3r 检测完成，正在合并结果...\033[0m'
addnum = 0
for domain in open("../input/domains.txt",'r').readlines():
    ### 判断./output 中是否存在文件，不存在则新建
    if not os.path.exists("../output/" + domain.replace("\n","") + ".txt"):
        file = open("../output/" + domain.replace("\n","") + ".txt", 'wr')
        file.close()
    if not os.path.exists("./output/" + domain.replace("\n","") + ".txt2"):
        file = open("./output/" + domain.replace("\n","") + ".txt2", 'wr')
        file.close()

    f_Sublist3r_out = open("./output/" + domain.replace("\n","") + ".txt2", 'r')
    for s1sublist3r_out in f_Sublist3r_out.readlines():
        signal = 1
        for s1out in open("../output/" + domain.replace("\n","") + ".txt", 'r').readlines(): #
            if s1sublist3r_out.replace("\n","") in s1out:
                signal = 0
                break

        if signal == 1:
            print  "新增 ",s1sublist3r_out.replace("\n","")
            open("../output/" + domain.replace("\n","") + ".txt", 'a+').write(s1sublist3r_out)
            addnum +=1
        # if signal == 0:
        #     print s1sublist3r_out.replace("\n", ""), "存在"

    ### 去除报告中的ip 和空格等
    f_report = open("../output/" + domain.replace("\n","") + ".txt", 'rw')
    open("../tmp/tmp1.txt", 'w').truncate()
    for line in f_report.readlines():
        # print line
        newline = re.sub("((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}", "",
                         line).replace(" ", "").replace(",", "")
        # f_domains.write(newline)

        open("../tmp/tmp1.txt", 'a+').write(newline)
    f_report.close()

    open("../output/" + domain.replace("\n","") + ".txt", 'w').truncate()
    for line2 in open("../tmp/tmp1.txt", 'r').readlines():
        open("../output/" + domain.replace("\n","") + ".txt", 'a+').write(line2)

print 'Sublist3r 新添加数量：',addnum
f_domains.close()