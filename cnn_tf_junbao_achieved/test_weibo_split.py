#!/usr/bin/env python
#coding:utf-8

import sys, os, stat
import re

MY_WORK_SPACE = os.environ['MY_WORK_SPACE']
sys.path.append(MY_WORK_SPACE)

from weibo_tokenizer import *

import json
import datetime
import string
import shutil

th = TokenizerHandler()
#res=th.split('\n警方缴获的毒品。记者史伟 通讯员应后威 摄\n贩毒团伙到汉即被监控 一举一动全在警方掌控中\n禁毒民警缴获92公斤海洛因\n贩毒团伙一到武汉，便被市公安局禁毒支队24小时侦控，在汉仅5天就被警方全部抓获，缴获海洛因92公斤。昨天，市公安局禁毒支队召开新闻发布会透露，这是近年来湖北警方一次性缴获毒品海洛因最多的一起案件。\n贩毒团伙一进武汉便被“盯上”\n今年5月，武汉市公安局禁毒支队通过大数据信息系统掌握了一个以刘某为首的湖南邵阳籍贩毒团伙，该团伙将在8月从境外运输毒品到国内，经湖南、武汉，销往西北。禁毒支队民警立即锁定该团伙，并对其进行严密监控。\n8月11日，刘某等4人刚一到汉，便立即进入警方的24小时侦控中。13日上午，民警得知刘某安排人前往东西湖区一建材市场“送货”，自己则到附近酒店收钱。专班民警兵分两路，一路继续对刘某等人实施侦控，另一路则前往建材市场搜寻“送货”男子。在建材市场内，民警发现了一名20多岁拖行李箱的黑衣男子形迹可疑，并在行李箱内发现22公斤毒品海洛因。另一路民警也在布控的酒店内将刘某等3人控制，现场收缴毒资220万余元。\n5天时间端掉跨省贩毒团伙\n刘某交代，另有一批毒品由同伙赵某看管。经过连续3天的视频分析和实地走访，发现13日晚赵某携带3个黑色袋子进入汉阳某小区后再未外出。8月15日早6点，民警将正准备出门的赵某及其马仔许某抓获，现场收缴毒品海洛因70余公斤、冰毒6公斤、毒资50余万元。\n目前，刘某、赵某等6名犯罪嫌疑人已被依法刑事拘留。据禁毒支队相关负责人介绍，该案是近年来我省警方一次性缴获毒品海洛因最多的一起案件。\n记者杨蔚 通讯员冯威 黄赤橙 盛达\n实习生王静文\n \n',tag_human_readable=False)
res=th.split('《三生三世十里桃花》白浅夜华为阿离醉酒',tag_human_readable=False)
#res = [x for x in res if x['pos_tag'] == 108]
#res=th.split('官方释疑雷洋案涉案警员免遭起诉:过失而非李三思故意 编辑 李逍遥',tag_human_readable=False,pid=167)
res = [x['word'] for x in res ]
#print json.dumps(res,indent=4,ensure_ascii=False)
print ' '.join(res)
