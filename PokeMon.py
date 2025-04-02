import heapq
import json
import random
import tkinter as tk
from tkinter import messagebox,simpledialog
import time
import ast
import sys
from datetime import datetime
from functools import lru_cache
import tkinter as tk
from fuzzywuzzy import process
from tkinter import Toplevel, Label, Entry, Listbox, Button, END
from tkinter import Toplevel, Label, Entry, Listbox, Button, StringVar, OptionMenu
import shutil
from tkinter import filedialog, messagebox
import os
from tkinter import simpledialog  # 引入 simpledialog 模块
from heapq import nlargest
global health_table
global damage_dict
GGG=0
GGGG=0
weather_effects = {
    "重力太空": ["暗", "电"],
    "极热沙漠": ["水", "草"],
    "暗黑界域": ["火", "光"],
    "海洋之星": ["火", "力"],
    "藤蔓之眼": ["力", "水"],
    "光明城堡": ["电", "暗"],
    "雷霆风暴": ["光", "草"],
    "众生平等": ["光", "草","暗", "电","火", "力","水"]
}
class Pokemon:
    def __init__(self, name, health, attribute, skill1, skill2, special_skill1,special_skill2, weaknesses, resistances,skill1type,skill2type,total):
        self.name = name
        self.health = health
        self.attribute = attribute
        self.skill1 = skill1  # (攻击值, 消耗点数)
        self.skill2 = skill2  # (攻击值, 消耗点数)
        self.special_skill1 = special_skill1  # 特殊技能（如 "盾牌", "反射伤害", "无"）
        self.special_skill2 = special_skill2  # 特殊技能（如 "盾牌", "反射伤害", "无"）
        self.weaknesses = weaknesses  # 弱点属性列表
        self.resistances = resistances  # 抵抗属性列表
        self.total_points = total  # 随机点数
        self.burned = False  # 是否被燃烧
        self.waiting = False  # 是否在等待回合
        self.score=0#循环赛积分
        self.orginhealth=self.health
        self.scorelist = [0, 0, 0]  # 循环赛胜负平记录
        self.shuyinglist = [[0], [0], [0]]  # 循环赛胜负平记录
        self.person_score = 0  # 个人积分
        self.person_paiming = 1000  # 个人积分
        self.skill1type = skill1type  # 技能类型（如 "杂", "纯"）
        self.skill2type = skill2type  # 技能类型（如 "杂", "纯"）
        self.special_skill1type = self.chaxun()[0]  # 特殊技能类型（如 "盾牌", "反射伤害", "无"）
        self.special_skill2type = self.chaxun()[1]  # 特殊技能类型（如 "盾牌", "反射伤害", "无"）
        self.useskill=None
    def apply_burn(self):
        """应用燃烧效果"""
        if self.burned:
            self.health -= 10  # 每回合燃烧造成10点伤害
    def get_special_skill_effect1(self):
        """获取特殊技能效果"""
        effects = {
            "盾牌": self.shield,
            "反射伤害": self.reflect_damage,
            "急速攻击": self.sprint_attack,
            "治疗": self.heal,
            "克制": self.kezhi,
            "燃烧": self.burn,
            "无": None
        }
        return effects.get(self.special_skill1, None)
    def get_special_skill_effect2(self):
        """获取特殊技能效果"""
        effects = {
            "盾牌": self.shield,
            "反射伤害": self.reflect_damage,
            "急速攻击": self.sprint_attack,
            "治疗": self.heal,
            "克制": self.kezhi,
            "燃烧": self.burn,
            "无": None
        }
        return effects.get(self.special_skill2, None)
    import random
    def chaxun(self):
        special_skilllist1 = ["燃烧"]
        special_skilllist2 = ["急速攻击"]
        special_skilllist3 = ["治疗"]
        special_skilllist4 = ["盾牌", "反射伤害"]
        special_skilllist5 = ["克制"]
        special_skilllist6 = ["无"]
        indexlist=[0,0]
        special_skilllist = [special_skilllist1, special_skilllist2, special_skilllist3, special_skilllist4,special_skilllist5,special_skilllist6]
        for i in range(len(special_skilllist)):
            for j in special_skilllist[i]:
                if(j==self.special_skill1):
                    indexlist[0]=i
                    self.special_skill1type=i
                if (j == self.special_skill2):
                    indexlist[1]=i
                    self.special_skill2type = i
        return indexlist
    def shield(self, damage):
        """盾牌效果，减少50%伤害"""
        return damage * 0.5
    def kezhi(self,type):
        """盾牌效果，减少50%伤害"""
        if(type=='skill1'and self.special_skill1=='克制'):
            return self.skill1[0]
        if (type == 'skill2' and self.special_skill2 == '克制'):
            return self.skill2[0]
    def reflect_damage(self, damage):
        """反射伤害效果，反弹50%伤害"""
        return damage * 0.5  # 返回反弹的伤害
    def sprint_attack(self, base_damage):
        """急速攻击，增加20%的攻击值"""
        return base_damage * 1.2  # 增加 20% 攻击值
    def heal(self):
        """治疗效果，恢复 30 点生命值"""
        heal_amount = 30
        a= self.health
        self.health +=min(a+heal_amount,health_table[self.name])
    def burn(self):
        """燃烧效果，给对方宝可梦施加燃烧状态"""
        self.burned = True
    def __str__(self):
        return f"宝可梦: {self.name}, 属性: {self.attribute}, 生命值: {self.health}, 技能1: {self.skill1[0]}, 技能1消耗点数: {self.skill1[1]}, 技能2: {self.skill2[0]}, 技能2消耗点数: {self.skill2[1]} 特殊技能1: {self.special_skill1}, 特殊技能2: {self.special_skill2}"
def save_most_used_skill(pokemon_list, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for pokemon in pokemon_list:
            if pokemon.useskill is not None:
                file.write(f"{pokemon.name}: {pokemon.useskill}\n")
class T_EAM:
    def __init__(self, name, members):
        self.name = name  # 团体名称
        self.members = members  # 团体成员（宝可梦列表）
        self.namelist=[mem.name for mem in members]
        self.team_score = 0  # 团体的总积分
        self.rank = None  # 团体排名
        self.win_count = 0  # 团体胜利次数
        self.loss_count = 0  # 团体失败次数
class Rank:
    def __init__(self):
        self.pokemon_rankings = {}
        self.team2_rankings = {}
        self.team3_rankings = {}
        self.team5_rankings = {}
        self.team7_rankings = {}
        self.team2_names = list(self.team2_rankings.keys())
        self.team3_names = list(self.team3_rankings.keys())
        self.team5_names = list(self.team5_rankings.keys())
        self.team7_names = list(self.team7_rankings.keys())
    def update_pokemon_rank(self,pokemon):
        self.pokemon_rankings[pokemon.name] = pokemon.person_score
        self.pokemon_rankings = dict(sorted(self.pokemon_rankings.items(), key=lambda x: x[1], reverse=True))
    def update_pok_rank(self):
        self.pokemon_rankings = dict(sorted(self.pokemon_rankings.items(), key=lambda x: x[1], reverse=True))
    def update_pokemon_rank1(self,pokemon):
        self.pokemon_rankings[pokemon.name] += pokemon.person_score
        self.pokemon_rankings = dict(sorted(self.pokemon_rankings.items(), key=lambda x: x[1], reverse=True))
    def update_team_rank(self, team, team_size):
        if team_size == 2:
            self.team2_rankings[team.name] = team
            self.team2_rankings = dict(sorted(self.team2_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        elif team_size == 3:
            self.team3_rankings[team.name] = team
            self.team3_rankings = dict(sorted(self.team3_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        elif team_size == 5:
            self.team5_rankings[team.name] = team
            self.team5_rankings = dict(sorted(self.team5_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        elif team_size == 7:
            self.team7_rankings[team.name] = team
            self.team7_rankings = dict(sorted(self.team7_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        else:
            raise ValueError("不支持的团体规模")
    def generate_team_name(self, team_type):
        """根据队伍类型自动生成队伍名称"""
        if team_type == 2:  # 双排队伍
            team_list = self.team2_names
            team_prefix = "双排队伍"
        elif team_type == 3:  # 三排队伍
            team_list = self.team3_names
            team_prefix = "三排队伍"
        elif team_type == 5:  # 五排队伍
            team_list = self.team5_names
            team_prefix = "五排队伍"
        elif team_type == 7:  # 七排队伍
            team_list = self.team7_names
            team_prefix = "七排队伍"
        else:
            raise ValueError("队伍类型错误")
        team_name = f"{team_prefix}{len(team_list) + 1}"
        team_list.append(team_name)  # 添加队伍名称到相应列表
        return team_name
    def add_pokemon(self, pokemon):
        """添加新的宝可梦及其得分"""
        self.pokemon_rankings[pokemon.name] = pokemon.person_score
        self.pokemon_rankings = dict(sorted(self.pokemon_rankings.items(), key=lambda x: x[1], reverse=True))
    def add_team(self, team, team_size):#读取时添加
        """添加新的团队"""
        if team_size == 2:
            self.team2_rankings[team.name] = team
            self.team2_rankings=dict(sorted(self.team2_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        elif team_size == 3:
            self.team3_rankings[team.name] = team
            self.team3_rankings = dict(sorted(self.team3_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        elif team_size == 5:
            self.team5_rankings[team.name] = team
            self.team5_rankings = dict(sorted(self.team5_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        elif team_size == 7:
            self.team7_rankings[team.name] = team
            self.team7_rankings = dict(sorted(self.team7_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        else:
            raise ValueError("不支持的团体规模")
    def add_team1(self, team, team_size):#运行时添加
        team_name = self.generate_team_name(team_size)
        """添加新的团队"""
        if team_size == 2:
            team.name=team_name
            self.team2_rankings[team.name] = team
            self.team2_rankings=dict(sorted(self.team2_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        elif team_size == 3:
            team.name = team_name
            self.team3_rankings[team.name] = team
            self.team3_rankings = dict(sorted(self.team3_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        elif team_size == 5:
            team.name = team_name
            self.team5_rankings[team.name] = team
            self.team5_rankings = dict(sorted(self.team5_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        elif team_size == 7:
            team.name = team_name
            self.team7_rankings[team.name] = team
            self.team7_rankings = dict(sorted(self.team7_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
        else:
            raise ValueError("不支持的团体规模")
    def get_pokemon_rank(self, pokemon_name):
        COUNT=1
        for name, score in self.pokemon_rankings.items():
            print(name, score)
            if pokemon_name == name:
                return COUNT, score
            COUNT += 1
        else:
            return None,None
    def get_team_rank(self, team_name, team_size):
        if team_size == 2:
            rankings_dict = self.team2_rankings
        elif team_size == 3:
            rankings_dict = self.team3_rankings
        elif team_size == 5:
            rankings_dict = self.team5_rankings
        elif team_size == 7:
            rankings_dict = self.team7_rankings
        else:
            raise ValueError("不支持的团体规模")
        COUNT = 1
        for name, score in rankings_dict.items():
            COUNT += 1
            if team_name ==name:
                return COUNT,score
            COUNT += 1
        else:
            return None,None
    def print_pokemon_rankings(self):
        print("个人排名：")
        COUNT=1
        for name, score in self.pokemon_rankings.items():
            print(f"{name} - 个人排名: {COUNT}- 得分: {score}")
            COUNT += 1
    def print_team2_rankings(self):
        print("2人团体排名：")
        for name, score in self.team2_rankings.items():
            print(f"{name} - 成员: {score.namelist}- 团队得分: {score.team_score}")
    def print_team3_rankings(self):
        print("3人团体排名：")
        for name, score in self.team3_rankings.items():
            print(f"{name} - 成员: {score.namelist}- 团队得分: {score.team_score}")
    def print_team5_rankings(self):
        print("5人团体排名：")
        for name, score in self.team5_rankings.items():
            print(f"{name} - 成员: {score.namelist}- 团队得分: {score.team_score}")
    def print_team7_rankings(self):
        print("7人团体排名：")
        for name, score in self.team7_rankings.items():
            print(f"{name} - 成员: {score.namelist}- 团队得分: {score.team_score}")
# def calculate_damage(attacker, defender, skill_type='skill1', skill_type1='skill1'):
#     """
#     计算攻击者攻击防守者时的伤害，包含属性弱点和抵抗的处理
#     """
#     skill_points = getattr(attacker, skill_type)[1]
#     if attacker.total_points < skill_points:
#         return 0  # 如果点数不足，无法攻击
#     attacker.total_points -= skill_points
#     base_damage =0
#     attack_diff = 0
#     if(skill_type=='skill1'):
#         base_damage = getattr(attacker, skill_type)[0]
#         special_effect = attacker.get_special_skill_effect1()
#         if special_effect == attacker.sprint_attack:
#             base_damage= special_effect(base_damage)
#         base_damage1 = getattr(defender, skill_type1)[0]
#         if(skill_type1=='skill1'):
#             special_effect1 = defender.get_special_skill_effect1()
#             if special_effect1 == defender.sprint_attack:
#                 base_damage1 = special_effect1(base_damage1)
#         elif (skill_type1 == 'skill2'):
#             special_effect1 = defender.get_special_skill_effect2()
#             if special_effect1 == defender.sprint_attack:
#                 base_damage1 = special_effect1(base_damage1)
#         attack_diff = base_damage - base_damage1
#         if special_effect:
#             if special_effect == attacker.heal:
#                 special_effect()  # 治疗不造成伤害
#             elif special_effect == attacker.sprint_attack:
#                 pass
#             elif (special_effect == attacker.kezhi) :
#                 if(skill_type1=='skill1' and defender.skill1type==1) :
#                      attack_diff= special_effect(skill_type)
#                 elif(skill_type1=='skill2' and defender.skill2type==1) :
#                      attack_diff= special_effect(skill_type)
#             elif special_effect == attacker.burn:
#                 attacker.burn()
#                 if (attacker.burned):
#                     attack_diff += 10
#             else:
#                 if (attack_diff > 0):
#                     pass
#                 else:
#                     attack_diff = special_effect(attack_diff)
#         if(special_effect!=attacker.kezhi ):
#             if (skill_type1 == 'skill1' and defender.special_skill1 == '反射伤害'):
#                 if(attack_diff>0):
#                     special_effect1 = defender.get_special_skill_effect1()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill1' and defender.special_skill1 == '盾牌'):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect1()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill2' and defender.special_skill2 == '反射伤害'):
#                 if(attack_diff>0):
#                     special_effect1 = defender.get_special_skill_effect2()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill2' and defender.special_skill2 == '盾牌'):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect2()
#                     attack_diff = special_effect1(attack_diff)
#         elif(special_effect==attacker.kezhi ):
#             if (skill_type1 == 'skill1' and defender.special_skill1 == '反射伤害')and (defender.skill1type!=0):
#                 if(attack_diff>0):
#                     special_effect1 = defender.get_special_skill_effect1()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill1' and defender.special_skill1 == '盾牌')and (defender.skill1type!=0):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect1()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill2' and defender.special_skill2 == '反射伤害')and (defender.skill2type!=0):
#                 if(attack_diff>0):
#                     special_effect1 = defender.get_special_skill_effect2()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill2' and defender.special_skill2 == '盾牌')and (defender.skill2type!=0):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect2()
#                     attack_diff = special_effect1(attack_diff)
#     if (skill_type == 'skill2'):
#         base_damage = getattr(attacker, skill_type)[0]
#         special_effect = attacker.get_special_skill_effect2()
#         if special_effect == attacker.sprint_attack:
#             base_damage = special_effect(base_damage)
#         base_damage1 = getattr(defender, skill_type1)[0]
#         if (skill_type1 == 'skill1'):
#             special_effect1 = defender.get_special_skill_effect1()
#             if special_effect1 == defender.sprint_attack:
#                 base_damage1 = special_effect1(base_damage1)
#         elif (skill_type1 == 'skill2'):
#             special_effect1 = defender.get_special_skill_effect2()
#             if special_effect1 == defender.sprint_attack:
#                 base_damage1 = special_effect1(base_damage1)
#         attack_diff = base_damage - base_damage1
#         if special_effect:
#             if special_effect == attacker.heal:
#                 special_effect()
#             elif special_effect == attacker.sprint_attack:
#                 pass
#             elif (special_effect == attacker.kezhi):
#                 if (skill_type1 == 'skill1' and defender.skill1type == 1):
#                     attack_diff = special_effect(skill_type)
#                 elif (skill_type1 == 'skill2' and defender.skill2type == 1):
#                     attack_diff = special_effect(skill_type)
#             elif special_effect == attacker.burn:
#                 if (attacker.burned):
#                     attack_diff += 10
#                 attacker.burn()  # 燃烧是状态改变，不需要传递伤害差值
#             else:
#                 if (attack_diff > 0):
#                     pass
#                 else:
#                     attack_diff = special_effect(attack_diff)
#         if (special_effect != attacker.kezhi):
#             if (skill_type1 == 'skill1' and defender.special_skill1 == '反射伤害'):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect1()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill1' and defender.special_skill1 == '盾牌'):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect1()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill2' and defender.special_skill2 == '反射伤害'):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect2()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill2' and defender.special_skill2 == '盾牌'):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect2()
#                     attack_diff = special_effect1(attack_diff)
#         elif (special_effect == attacker.kezhi):
#             if (skill_type1 == 'skill1' and defender.special_skill1 == '反射伤害') and (defender.skill1type != 0):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect1()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill1' and defender.special_skill1 == '盾牌') and (defender.skill1type != 0):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect1()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill2' and defender.special_skill2 == '反射伤害') and (defender.skill2type != 0):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect2()
#                     attack_diff = special_effect1(attack_diff)
#             elif (skill_type1 == 'skill2' and defender.special_skill2 == '盾牌') and (defender.skill2type != 0):
#                 if (attack_diff > 0):
#                     special_effect1 = defender.get_special_skill_effect2()
#                     attack_diff = special_effect1(attack_diff)
#     if (defender.waiting):
#         if (skill_type == 'skill1'):
#             base_damage = getattr(attacker, skill_type)[0]
#             special_effect = attacker.get_special_skill_effect1()
#             if special_effect == attacker.sprint_attack:
#                 base_damage = special_effect(base_damage)
#             if special_effect == attacker.burn:
#                 base_damage+=10
#         if (skill_type == 'skill2'):
#             base_damage = getattr(attacker, skill_type)[0]
#             special_effect = attacker.get_special_skill_effect2()
#             if special_effect == attacker.sprint_attack:
#                 base_damage = special_effect(base_damage)
#             if special_effect == attacker.burn:
#                 base_damage += 10
#         attack_diff = base_damage
#     damage=0
#     if( attack_diff>0):
#         if attacker.attribute in defender.weaknesses:
#             damage = max(attack_diff + 30, 0)
#         elif attacker.attribute in defender.resistances or(defender.resistances=="全"):
#             damage = max(attack_diff - 30, 0)
#         else:
#             damage = max(attack_diff, 0)
#     if(damage<0):
#         damage=0
#     return damage
def special_c1(pokemon,type):#计算急速攻击，燃烧等特殊技能,获取每个个体的攻击值
    special_effect = pokemon.get_special_skill_effect1() if type == 'skill1' else pokemon.get_special_skill_effect2()


    base_damage = getattr(pokemon, type)[0]#获得伤害

    if special_effect == pokemon.sprint_attack:
        base_damage = special_effect(base_damage)
    if special_effect == pokemon.burn:
        pokemon.burn()
        if (pokemon.burned):
            base_damage += 10
    # if (type == 'skill2'):
    #     base_damage = getattr(pokemon, type)[0]  # 获得伤害
    #     special_effect = pokemon.get_special_skill_effect2()
    #     if special_effect == pokemon.sprint_attack:
    #         base_damage = special_effect(base_damage)
    #     if special_effect == pokemon.burn:
    #         pokemon.burn()
    #         if (pokemon.burned):
    #             base_damage += 10
    return base_damage
def special_c2(pokemon1,type1,pokemon2,type2,attack_diff,d1):#计算克制等特殊技能
    if (type1 == 'skill1'):
        special_effect1 = pokemon1.get_special_skill_effect1()
        if (special_effect1 == pokemon1.kezhi):
            if (type2 == 'skill1' and pokemon2.skill1type == 1):
                attack_diff =d1
                # attack_diff = special_c1(pokemon1,type1)
            elif (type2 == 'skill2' and pokemon2.skill2type == 1):
                attack_diff = d1
                # attack_diff =special_c1(pokemon1,type1)
    if (type1 == 'skill2'):
        special_effect1 = pokemon1.get_special_skill_effect2()
        if (special_effect1 == pokemon1.kezhi):
            if (type2 == 'skill1' and pokemon2.skill1type == 1):
                attack_diff = d1
                # attack_diff = special_c1(pokemon1, type1)
            elif (type2 == 'skill2' and pokemon2.skill2type == 1):
                attack_diff = d1
                # attack_diff = special_c1(pokemon1, type1)
    return attack_diff
def special_c3(pokemon2,type2,attack_diff):#计算反射，盾牌，治疗等特殊技能
    #在这一步计算已经完成，对结果进行修正，结果<0时进行治疗特殊技能使用，>0时用反射，盾牌，治疗,均为单项技能

    if (type2 == 'skill1' and pokemon2.get_special_skill_effect1() == pokemon2.heal):
        pokemon2.heal()
    elif (type2 == 'skill2' and pokemon2.get_special_skill_effect1() == pokemon2.heal):
        pokemon2.heal()
    if (type2 == 'skill1' and pokemon2.get_special_skill_effect1() == pokemon2.shield):
        attack_diff=pokemon2.shield(attack_diff)
    elif (type2 == 'skill2' and pokemon2.get_special_skill_effect2() == pokemon2.shield):
        attack_diff=pokemon2.shield(attack_diff)
    if (type2 == 'skill1' and pokemon2.get_special_skill_effect1() == pokemon2.reflect_damage):
        attack_diff=pokemon2.reflect_damage(attack_diff)
    elif (type2 == 'skill2' and pokemon2.get_special_skill_effect2() == pokemon2.reflect_damage):
        attack_diff=pokemon2.reflect_damage(attack_diff)
    return attack_diff
def xiuding(attacker, defender,attack_diff):
    damage = 0
    if (attack_diff > 0):
        if attacker.attribute in defender.weaknesses:
            damage = max(attack_diff + 30, 0)
        elif attacker.attribute in defender.resistances or (defender.resistances == "全"):
            damage = max(attack_diff - 30, 0)
        else:
            damage = max(attack_diff, 0)
    if (damage <= 0):
        damage = 0
    return damage
def calculate_damage(attacker, defender, skill_type='skill1', skill_type1='skill1'):#单项计算，保证，攻击者造成的伤害是正确的
    skill_points = getattr(attacker, skill_type)[1]#攻击者消耗的点数
    if(attacker.total_points >=skill_points):#点数充足，攻击者可以进行攻击
        attacker.total_points -= skill_points  # 攻击者点数消耗
        d1 = special_c1(attacker, skill_type)
        #调用第一类特殊技能，攻击前进行攻击值修正
        if(defender.waiting==False):

            d2=special_c1(defender,skill_type1)
            attack_diff=d1-d2#第一类特殊技能，攻击前准备
            # print(attack_diff)
            #调用第二类特殊技能，对攻击值进行修正
            attack_diff = special_c2(attacker, skill_type,defender, skill_type1,attack_diff,d1)
            # if (skill_type == 'skill1'):
            #     special_effect1 = attacker.get_special_skill_effect1()
            #     if (special_effect1 == attacker.kezhi):
            #         if (skill_type1 == 'skill1' and defender.skill1type == 1):
            #             attack_diff = d1
            #             # attack_diff = special_c1(pokemon1,type1)
            #         elif (skill_type1 == 'skill2' and defender.skill2type == 1):
            #             attack_diff = d1
            #             # attack_diff =special_c1(pokemon1,type1)
            # if (skill_type == 'skill2'):
            #     special_effect1 = attacker.get_special_skill_effect2()
            #     if (special_effect1 == attacker.kezhi):
            #         if (skill_type1 == 'skill1' and defender.skill1type == 1):
            #             attack_diff = d1
            #             # attack_diff = special_c1(pokemon1, type1)
            #         elif (skill_type1 == 'skill2' and defender.skill2type == 1):
            #             attack_diff = d1
            attack_diff = special_c3(defender, skill_type1, attack_diff)
        else:
            attack_diff = d1
    else:return 0
    damage=xiuding(attacker, defender,attack_diff)
    return damage
def greedy_attack(pokemon, defender):
    """使用贪心算法选择最优技能进行攻击"""
    best_skill = None
    best_damage = -10000
    global mz
    available_skills_pokemon = []
    if pokemon.total_points >= getattr(pokemon, 'skill1')[1]:
        available_skills_pokemon.append('skill1')
    if pokemon.total_points >= getattr(pokemon, 'skill2')[1]:
        available_skills_pokemon.append('skill2')
    available_skills_defender = []
    if defender.total_points >= getattr(defender, 'skill1')[1]:
        available_skills_defender.append('skill1')
    if defender.total_points >= getattr(defender, 'skill2')[1]:
        available_skills_defender.append('skill2')
    if (available_skills_pokemon == []):
        print(pokemon.name, defender.name)
        print(pokemon.waiting, defender.waiting,"陷入陷阱")
    for skill_type in available_skills_pokemon:
        if(available_skills_defender==[]):
            available_skills_defender=['skill1','skill2']
        for skill_type1 in available_skills_defender:
            damage = calculate_damage(pokemon, defender, skill_type=skill_type, skill_type1=skill_type1)
            if(damage>0):
                if damage > best_damage:
                    best_damage = damage
                    best_skill = skill_type
    if best_damage <= 0:
        if(len(available_skills_pokemon)>1):
            if( getattr(pokemon, 'skill1')[0]> getattr(pokemon, 'skill2')[0]):
                best_skill = 'skill1'
            else:best_skill = 'skill2'
        else: best_skill = available_skills_pokemon[0]
        best_damage = 0
    return best_skill, best_damage
def greedy_attack1(pokemon):
    """使用贪心算法选择最优技能进行攻击"""
    if (getattr(pokemon,'skill1')[0]/float(getattr(pokemon, 'skill1')[1])) > (getattr(pokemon,'skill2')[0]/float(getattr(pokemon, 'skill2')[1])):
        return 'skill1'
    else:return 'skill2'
def battle(pokemon1, pokemon2,moshi,selected_weather):
    # print(health_table[pokemon1.name])
    global GGGG
    battle_output = []
    round_limit = 5
    flag1=False
    flag2 =False
    flag_1 = True
    flag_2 = True
    g_skill1=None
    g_skill2=None
    g_damge1 = 0
    g_damge2 = 0
    pokemon1.total_points=random.randint(9,15)
    pokemon2.total_points = random.randint(9, 15)
    if(selected_weather!="正常天气"):
        affected_attributes = weather_effects[selected_weather]
        if (str(pokemon1.attribute) in affected_attributes):
            battle_output.append(f"受天气影响 {pokemon1.name} 初始生命值降低10点，攻击值降低10点")
            pokemon1.health=pokemon1.health-10
            pokemon1.skill1 = (pokemon1.skill1[0] - 10, pokemon1.skill1[1])
            pokemon1.skill2 = (pokemon1.skill2[0] - 10, pokemon1.skill2[1])
        if (str(pokemon2.attribute) in affected_attributes):
            battle_output.append(f"受天气影响 {pokemon2.name} 初始生命值降低10点，攻击值降低10点")
            pokemon2.health=pokemon2.health-10
            pokemon2.skill1 = (pokemon2.skill1[0] - 10, pokemon2.skill1[1])
            pokemon2.skill2 = (pokemon2.skill2[0] - 10, pokemon2.skill2[1])
    if(moshi=="克隆模式"):
        aaa= random.randint(9, 15)
        pokemon1.total_points =  aaa
        pokemon2.total_points =  aaa
    a=1
    b=1
    for round_num in range(round_limit):
        battle_output.append(f" {pokemon1.name} 初始生命值{pokemon1.health},初始点数{pokemon1.total_points}")
        battle_output.append(f" {pokemon2.name} 初始生命值{pokemon2.health},初始点数{pokemon2.total_points}")
        if pokemon1.health <= 0 or pokemon2.health <= 0:
            break
        pokemon1.apply_burn()
        pokemon2.apply_burn()
        battle_output.append(str(f"--- 轮次 {round_num + 1} ---"))
        huihe=1
        n1=1
        n2=1
        while not pokemon1.waiting and not pokemon2.waiting:
            # print(huihe)
            if(huihe>25):
                # print(pokemon1,pokemon2)
                # print(pokemon1.total_points, pokemon2.total_points)
                # print(flag1, flag2)
                exit()
            if((pokemon1.useskill !=None) and (pokemon1.useskill !="None")):
                g_skill1 = pokemon1.useskill
            else:
                pokemon_1=Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1, pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type, pokemon1.skill2type,pokemon1.total_points)
                pokemon_2=Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1, pokemon2.skill2,pokemon2.special_skill1,pokemon2.special_skill2, pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type, pokemon2.skill2type,pokemon2.total_points)
                if (flag1 == False):
                    skill1, damage_1 = greedy_attack(pokemon_1, pokemon_2)
                    if(a==1 and GGGG==1):
                        pokemon1.useskill=skill1
                    g_skill1 = skill1
            if ((pokemon2.useskill !=None) and (pokemon2.useskill !="None")):
                g_skill2 = pokemon2.useskill
            else:
                pokemon_11 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1, pokemon1.skill2,pokemon1.special_skill1, pokemon1.special_skill2, pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type, pokemon1.skill2type,pokemon1.total_points)
                pokemon_22 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1, pokemon2.skill2,pokemon2.special_skill1,pokemon2.special_skill2, pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type, pokemon2.skill2type,pokemon2.total_points)
                if (flag2 == False):
                    skill2, damage_2 = greedy_attack(pokemon_22, pokemon_11)
                    g_skill2 = skill2
                    if (b == 1 and GGGG == 1):
                        pokemon2.useskill = skill1
            # if(flag1==False):
            #     skill1, damage_1 = greedy_attack(pokemon_1, pokemon_2)
            #
            #     g_skill1=skill1
            #     # pokemon1.useskill = g_skill1
            # if (flag2 == False):
            #
            #     skill2, damage_2 = greedy_attack(pokemon_22, pokemon_11)
            #     g_skill2=skill2
            #     # pokemon2.useskill = g_skill2
            battle_output.append(f"-- 回合 {huihe} --")
            a+=1
            b+=1

            if(flag_1 == False ):
                pokemon_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                    pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                    pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type, pokemon1.skill2type,
                                    pokemon1.total_points)
                pokemon_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1,
                                    pokemon2.skill2, pokemon2.special_skill1, pokemon2.special_skill2,
                                    pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type, pokemon2.skill2type,
                                    pokemon2.total_points)

                skill1, damage_1 = greedy_attack(pokemon_1, pokemon_2)
                g_skill1 = skill1
            if (flag_2 == False):
                pokemon_11 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                     pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                     pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type,
                                     pokemon1.skill2type, pokemon1.total_points)
                pokemon_22 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1,
                                     pokemon2.skill2, pokemon2.special_skill1, pokemon2.special_skill2,
                                     pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type,
                                     pokemon2.skill2type, pokemon2.total_points)

                skill2, damage_2 = greedy_attack(pokemon_22, pokemon_11)
                g_skill2 = skill2

            if (flag1 == False):
                damage1=calculate_damage(pokemon1, pokemon2, g_skill1, g_skill2)#1对2造成的伤害

                g_damge1=damage1
                pokemon1.total_points += getattr(pokemon1, g_skill1)[1]

            if (flag2 == False):
                damage2 = calculate_damage(pokemon2, pokemon1, g_skill2, g_skill1)  # 2对1造成的伤害
                g_damge2 = damage2
                pokemon2.total_points += getattr(pokemon2, g_skill2)[1]


            pokemon2.health -= g_damge1
            pokemon1.health -= g_damge2
            pokemon1.total_points-=getattr(pokemon1, g_skill1)[1]
            pokemon2.total_points -= getattr(pokemon2, g_skill2)[1]
            battle_output.append(f"{pokemon1.name} 使用了技能对{pokemon2.name}造成 {g_damge1} 点伤害")
            battle_output.append(f"{pokemon2.name} 使用了技能对{pokemon1.name} 造成 {g_damge2} 点伤害")
            battle_output.append(f"{pokemon1.name} 剩余生命值{pokemon1.health},剩余点数{pokemon1.total_points}")
            battle_output.append(f"{pokemon2.name} 剩余生命值{pokemon2.health},剩余点数{pokemon2.total_points}")
            if pokemon1.health <= 0 and pokemon2.health <= 0:
                battle_output.append("平局")
                return "平局", battle_output,"0"
            elif pokemon1.health < 0 and pokemon2.health > 0:
                battle_output.append(f"{pokemon2.name} 胜利")
                return f"{pokemon2.name} 胜利", battle_output,"2"
            elif pokemon2.health < 0 and pokemon1.health > 0:
                battle_output.append(f"{pokemon1.name} 胜利")
                return f"{pokemon1.name} 胜利", battle_output,"1"
            if(( pokemon1.total_points >= getattr(pokemon1, 'skill1')[1]) and (pokemon1.total_points >= getattr(pokemon1, 'skill2')[1])):  # print(f"{pokemon2.name} 点数用完，进入等待状态。")
                flag1 = True
            if ((pokemon2.total_points >= getattr(pokemon2, 'skill1')[1] )and( pokemon2.total_points >=getattr(pokemon2, 'skill2')[1])):  # print(f"{pokemon2.name} 点数用完，进入等待状态。")
                flag2=True
            if ((pokemon1.total_points >=getattr(pokemon1, 'skill1')[1]) and ( pokemon1.total_points < getattr(pokemon1, 'skill2')[1])):  # print(f"{pokemon2.name} 点数用完，进入等待状态。")
                if(g_skill1=='skill2'):
                    flag1 = False
                    flag_1=False
            if ((pokemon1.total_points < getattr(pokemon1, 'skill1')[1]) and (pokemon1.total_points >=getattr(pokemon1, 'skill2')[1])):  # print(f"{pokemon2.name} 点数用完，进入等待状态。")
                if (g_skill1 == 'skill1'):
                    flag1 = False
                    flag_1 = False
            if ((pokemon2.total_points >= getattr(pokemon2, 'skill1')[1]) and (pokemon2.total_points < getattr(pokemon2, 'skill2')[1])):  # print(f"{pokemon2.name} 点数用完，进入等待状态。")
                if (g_skill2 == 'skill2'):
                    flag2 = False
                    flag_2 = False
            if ((pokemon2.total_points < getattr(pokemon2, 'skill1')[1]) and (pokemon2.total_points >= getattr(pokemon2, 'skill2')[1])):  # print(f"{pokemon2.name} 点数用完，进入等待状态。")
                if (g_skill2 == 'skill1'):
                    flag2 = False
                    flag_2 = False
            if ((pokemon2.total_points < getattr(pokemon2, 'skill1')[1]) or (
                    pokemon2.total_points < getattr(pokemon2, 'skill2')[1])):  # print(f"{pokemon2.name} 点数用完，进入等待状态。")
                flag2 = False
            if pokemon1.total_points < getattr(pokemon1, 'skill1')[1] and pokemon1.total_points < getattr(pokemon1, 'skill2')[1]:
                flag1 = False
                battle_output.append(f"{pokemon1.name} 点数用完，进入等待状态。")
                pokemon1.waiting = True
            if pokemon2.total_points < getattr(pokemon2, 'skill1')[1] and pokemon2.total_points <getattr(pokemon2, 'skill2')[1]: #print(f"{pokemon2.name} 点数用完，进入等待状态。")
                battle_output.append(f"{pokemon2.name} 点数用完，进入等待状态。")
                pokemon2.waiting = True
                flag2 = False
            huihe+=1
        while  pokemon1.waiting and not pokemon2.waiting:#宝可梦1处于等待状态
            if (huihe > 25):
                exit()
            pokemon_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1, pokemon1.skill2,
                                pokemon1.special_skill1, pokemon1.special_skill2, pokemon1.weaknesses,
                                pokemon1.resistances, pokemon1.skill1type, pokemon1.skill2type, pokemon1.total_points)
            pokemon_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1, pokemon2.skill2,
                                pokemon2.special_skill1, pokemon2.special_skill2, pokemon2.weaknesses,
                                pokemon2.resistances, pokemon2.skill1type, pokemon2.skill2type, pokemon2.total_points)
            if(flag2==False):
                skill2, damage_2 = greedy_attack(pokemon_2, pokemon_1)
                g_skill2=skill2
            # if (g_skill2 == "skill1"):
            #     k2_1 += 1
            # else:
            #     k2_2 += 1
            damage2 = calculate_damage(pokemon2, pokemon1, g_skill2, 'skill2')  # 2对1造成的伤害
            pokemon1.health -= damage2
            battle_output.append(f"-- 回合 {huihe} --")
            battle_output.append(f"{pokemon1.name} 点数用完，进入等待状态。")
            battle_output.append(f"    {pokemon2.name} 使用了技能对{pokemon1.name} 造成 {damage2} 点伤害")
            battle_output.append(f"    {pokemon1.name} 剩余生命值{pokemon1.health},剩余点数{pokemon1.total_points}")
            battle_output.append(f"    {pokemon2.name} 剩余生命值{pokemon2.health},剩余点数{pokemon2.total_points}")
            if pokemon1.health <= 0 and pokemon2.health <= 0:
                battle_output.append("平局")
                return "平局", battle_output, "0"
            elif pokemon1.health < 0 and pokemon2.health > 0:
                battle_output.append(f"{pokemon2.name} 胜利")
                return f"{pokemon2.name} 胜利", battle_output, "2"
            elif pokemon2.health < 0 and pokemon1.health >= 0:
                battle_output.append(f"{pokemon1.name} 胜利")
                return f"{pokemon1.name} 胜利", battle_output, "1"
            if pokemon2.total_points >= getattr(pokemon2, 'skill1')[1] and pokemon2.total_points >=getattr(pokemon2, 'skill2')[1]:
                flag2=True
            if pokemon2.total_points >= getattr(pokemon2, 'skill1')[1] and pokemon2.total_points <getattr(pokemon2, 'skill2')[1]:
                if (g_skill2 == 'skill2'):
                    flag2 = False
                    flag_2 = False
            if pokemon2.total_points < getattr(pokemon2, 'skill1')[1] and pokemon2.total_points >=getattr(pokemon2, 'skill2')[1]:
                if (g_skill2 == 'skill1'):
                    flag2 = False
            if pokemon2.total_points < getattr(pokemon2, 'skill1')[1] and pokemon2.total_points < getattr(pokemon2, 'skill2')[1]:
                flag2 = False
                flag_2 = False
                battle_output.append(f"{pokemon2.name} 点数用完，进入等待状态。")
                pokemon2.waiting = True
                break
            huihe += 1
        while not pokemon1.waiting and  pokemon2.waiting:#宝可梦二处于等待状态
            if (huihe > 25):
                exit()
            battle_output.append(f"-- 回合 {huihe} --")
            pokemon_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1, pokemon1.skill2,
                                pokemon1.special_skill1, pokemon1.special_skill2, pokemon1.weaknesses,
                                pokemon1.resistances, pokemon1.skill1type, pokemon1.skill2type, pokemon1.total_points)
            pokemon_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1, pokemon2.skill2,
                                pokemon2.special_skill1, pokemon2.special_skill2, pokemon2.weaknesses,
                                pokemon2.resistances, pokemon2.skill1type, pokemon2.skill2type, pokemon2.total_points)
            if (flag1 == False):
                skill1, damage_1 = greedy_attack(pokemon_1, pokemon_2)
                g_skill1 = skill1
            # if (g_skill1 == "skill1"):
            #     k1_1 += 1
            # else:
            #     k1_2 += 1
            damage1 = calculate_damage(pokemon1, pokemon2, g_skill1, 'skill2')  # 1对2造成的伤害
            pokemon2.health -=  damage1
            battle_output.append(f"{pokemon2.name} 点数用完，进入等待状态。")
            battle_output.append(f"    {pokemon1.name} 使用了技能对{pokemon2.name}造成 { damage1} 点伤害")
            battle_output.append(f"    {pokemon1.name} 剩余生命值{pokemon1.health},剩余点数{pokemon1.total_points}")
            battle_output.append(f"     {pokemon2.name} 剩余生命值{pokemon2.health},剩余点数{pokemon2.total_points}")
            if pokemon1.health <= 0 and pokemon2.health <= 0:
                battle_output.append("平局")
                return "平局", battle_output, "0"
            elif pokemon1.health < 0 and pokemon2.health > 0:
                battle_output.append(f"{pokemon2.name} 胜利")
                return f"{pokemon2.name} 胜利", battle_output, "2"
            elif pokemon2.health < 0 and pokemon1.health > 0:
                battle_output.append(f"{pokemon1.name} 胜利")
                return f"{pokemon1.name} 胜利", battle_output, "1"
            if pokemon1.total_points >= getattr(pokemon1, 'skill1')[1] and pokemon1.total_points >=getattr(pokemon1, 'skill2')[1]:
                flag1=True
            if pokemon1.total_points >= getattr(pokemon1, 'skill1')[1] and pokemon1.total_points <getattr(pokemon1, 'skill2')[1]:
                if (g_skill1 == 'skill2'):
                    flag1 = False
                    flag_1 = False
            if pokemon1.total_points < getattr(pokemon1, 'skill1')[1] and pokemon1.total_points >=getattr(pokemon1, 'skill2')[1]:
                if (g_skill1 == 'skill1'):
                    flag1 = False
                    flag_1 = False
            if pokemon1.total_points < getattr(pokemon1, 'skill1')[1] and pokemon1.total_points < getattr(pokemon1, 'skill2')[1]:
                flag1 = False
                pokemon1.waiting = True
                battle_output.append(f"{pokemon1.name} 点数用完，进入等待状态。")
                break
            huihe += 1
        if pokemon1.health <= 0 and pokemon2.health <= 0:
            battle_output.append("平局")
            return "平局", battle_output, "0"
        elif pokemon1.health < 0 and pokemon2.health >= 0:
            battle_output.append(f"{pokemon2.name} 胜利")
            return f"{pokemon2.name} 胜利", battle_output, "2"
        elif pokemon2.health < 0 and pokemon1.health > 0:
            battle_output.append(f"{pokemon1.name} 胜利")
            return f"{pokemon1.name} 胜利", battle_output, "1"
        else:
            bbb1 = random.randint(9, 15)
            if pokemon1.waiting and pokemon2.waiting:
                pokemon1.total_points = random.randint(9, 15)
                pokemon2.total_points = random.randint(9, 15)
                if (moshi == "克隆模式"):
                    pokemon1.total_points = bbb1
                    pokemon2.total_points = bbb1
                pokemon1.waiting = False
                pokemon2.waiting = False
                flag1 = False
                flag2 = False
                flag_1 = True
                flag_2 = True
    if pokemon1.health >= 0 and pokemon2.health >= 0:
        battle_output.append("平局")
        return "平局5", battle_output, "0"
    elif pokemon1.health <= 0 and pokemon2.health <= 0:
        battle_output.append("平局")
        return "平局", battle_output, "0"
    elif pokemon1.health <0 and pokemon2.health > 0:
        battle_output.append(f"{pokemon2.name} 胜利")
        return f"{pokemon2.name} 胜利", battle_output, "2"
    elif pokemon2.health < 0 and pokemon1.health > 0:
        battle_output.append(f"{pokemon1.name} 胜利")
        return f"{pokemon1.name} 胜利", battle_output, "1"
    else:
        battle_output.append("出错了")
        return None, battle_output,"0"
import random
attributes = ["力", "光", "暗", "火", "草", "水", "电"]
special_skills = ["盾牌", "反射伤害", "急速攻击", "治疗", "燃烧", "克制", "无"]
generated_names = set()
def generate_unique_name(attribute):
    while True:
        name = f"{attribute} 宝可梦 {random.randint(1, 100)}"
        if name not in generated_names:
            generated_names.add(name)
            return name
def generate_random_pokemon(attribute):
    name=generate_unique_name(attribute)
    health = random.randint(50, 300)
    skill1 = (random.randint(30, 250), random.randint(1, 4))  # (攻击值, 消耗点数)
    skill2 = (random.randint(30, 160), random.randint(1, 4))  # (攻击值, 消耗点数)
    skill1type=random.choices([0, 1], weights=[0.95, 0.05])[0]
    skill2type = random.choices([0, 1], weights=[0.95, 0.05])[0]
    special_skill1 = random.choice(special_skills)
    special_skill2 = random.choice([skill for skill in special_skills if skill != special_skill1]) if len(special_skills) > 1 else "无"
    attribute0 = ["力", "光", "暗", "火", "草", "水", "电", "无", ]
    attribute1=["力", "光", "暗", "火", "草", "水", "电","无","全"]
    weaknesses = random.sample([attr for attr in attribute0 if attr != attribute], 1)
    resistances = random.sample([attr for attr in attribute1 if attr != attribute], 1)
    total = random.randint(9, 15)
    return Pokemon(name, health, attribute, skill1, skill2, special_skill1, special_skill2, weaknesses, resistances,skill1type,skill2type,total)
def generate_and_save_pokemon_data(file_path="pokemons.txt"):
    all_pokemons = []
    for attribute in attributes:
        for _ in range(random.randint(40, 60)):  # 为每个属性生成 50-60 个宝可梦
            pokemon = generate_random_pokemon(attribute)
            all_pokemons.append(pokemon)
    with open(file_path, "w", encoding="utf-8") as f:
        for pkm in all_pokemons:
            f.write( f"{pkm.name},{pkm.health},{pkm.attribute},{pkm.skill1[0]},{pkm.skill1[1]},{pkm.skill2[0]},{pkm.skill2[1]},{pkm.special_skill1},{pkm.special_skill2 },{','.join(pkm.weaknesses)},{','.join(pkm.resistances)},{pkm.skill1type},{pkm.skill2type},{pkm.total_points}\n")
def write(pokemon,file_path="pokemons.txt"):
    with open(file_path, "w", encoding="utf-8") as f:
        for pkm in pokemon:
            f.write( f"{pkm.name},{pkm.health},{pkm.attribute},{pkm.skill1[0]},{pkm.skill1[1]},{pkm.skill2[0]},{pkm.skill2[1]},{pkm.special_skill1},{pkm.special_skill2 },{','.join(pkm.weaknesses)},{','.join(pkm.resistances)},{pkm.skill1type},{pkm.skill2type},{pkm.total_points}\n")


def load_pokemons_from_file1(file_path="pokemons.txt"):
    health_table = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            data = line.strip().split(',')
            name = data[0]
            health = int(data[1])
            health_table[name]=health
    return  health_table
def load_pokemons_from_file(file_path="pokemons.txt"):
    pokemons = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            data = line.strip().split(',')
            name = data[0]
            health = int(data[1])
            attribute = data[2]
            skill1 = (int(data[3]), int(data[4]))
            skill2 = (int(data[5]), int(data[6]))
            special_skill1 = data[7]
            special_skill2 = data[8]
            weaknesses = data[9].split(',')
            resistances = data[10].split(',')
            skill1type=int(data[11].split(',')[0])
            skill2type=int(data[12].split(',')[0])
            total = int(data[13].split(',')[0])
            pokemons.append(Pokemon(name, health, attribute, skill1, skill2, special_skill1, special_skill2, weaknesses, resistances,skill1type,skill2type,total))



    return pokemons

@profile
def round_robin_tournament(pokemon_list,K,moshi,whe):
    global GGG
    global GGGG
    start_time = time.time()
    print("开始循环赛")
    """进行循环积分赛制，并根据积分排序"""
    print(GGG,GGGG)
    if(K>=len(pokemon_list)and GGGG==1):
        GGG=1
    if(K>=len(pokemon_list)):
        count1=0
        for pokemon in pokemon_list:
            pokemon.score = 0
            pokemon.scorelist = [0, 0, 0]
            pokemon.shuyinglist = [[], [], []]  # 循环赛胜负平记录
        for i in range(len(pokemon_list)):
            for j in range(i,len(pokemon_list)):
                if(i!=j):
                    pokemon1 = pokemon_list[i]
                    pokemon2 = pokemon_list[j]
                    pokemon1_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                        pokemon1.skill2, pokemon1.special_skill1,pokemon1.special_skill2, pokemon1.weaknesses, pokemon1.resistances,pokemon1.skill1type,pokemon1.skill2type,pokemon1.total_points)
                    pokemon2_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1,
                                        pokemon2.skill2, pokemon2.special_skill1,pokemon2.special_skill2, pokemon2.weaknesses, pokemon2.resistances,pokemon2.skill1type,pokemon2.skill2type,pokemon2.total_points)
                    if(GGGG==0):
                        pokemon1_1.useskill=pokemon1.useskill
                        pokemon2_2.useskill = pokemon2.useskill
                    result, result1, result_2 = None, None, None


                    if (int(damage_dict[ pokemon1_1.name]['min_damage']) -int(damage_dict[ pokemon2_2.name]['max_damage'])  >  3* pokemon2_2.health):
                        result = f"{pokemon1_1.name} 胜利"
                        count1+=1
                    elif (int(damage_dict[pokemon2_2.name]['min_damage']) - int(damage_dict[pokemon1_1.name]['max_damage']) >3*pokemon1_1.health):
                        result = f"{pokemon2_2.name} 胜利"
                        count1 += 1
                    else:
                        result, result1, result_2 = battle(pokemon1_1, pokemon2_2, moshi, whe)
                    # result,result1,result_2 = battle(pokemon1_1, pokemon2_2,moshi,whe)
                    if(GGGG==1):
                        pokemon1.useskill=pokemon1_1.useskill
                        pokemon2.useskill=pokemon2_2.useskill
                    if result == f"{pokemon1_1.name} 胜利":
                        pokemon1.score += 3  # pokemon1 获胜
                        pokemon2.score += 0  # pokemon1 获胜
                        pokemon1.shuyinglist[0].append(pokemon2.name)
                        pokemon2.shuyinglist[2].append(pokemon1.name)
                        pokemon1.scorelist[0]+=1
                        pokemon2.scorelist[2] += 1
                    elif result == f"{pokemon2.name} 胜利":
                        pokemon1.score += 0  # pokemon2 获胜
                        pokemon2.score += 3  # pokemon2 获胜
                        pokemon1.shuyinglist[2].append(pokemon2.name)
                        pokemon2.shuyinglist[0].append(pokemon1.name)
                        pokemon1.scorelist[2] += 1
                        pokemon2.scorelist[0] += 1
                    else:
                        pokemon1.score += 1  # 平局
                        pokemon2.score += 1  # 平局
                        pokemon1.shuyinglist[1].append(pokemon2.name)
                        pokemon1. scorelist[1] += 1
                        pokemon2.shuyinglist[1].append(pokemon1.name)
                        pokemon2.scorelist[1] += 1
        print(count1)
    else:#K小于32,极限优化
        count1=0
        for pokemon in pokemon_list:
            pokemon.score = 3 * len(pokemon_list)
            pokemon.scorelist = [0, 0, 0]
            pokemon.shuyinglist = [[], [], []]  # 循环赛胜负平记录
        if K < 5:
             theta = 3*10 * K
        elif K>=5 and K < 10:
            theta =  3* 8*K
        elif K>=10 and K <= 64:
            theta = 3* (K+20)
        elif K>=64 and K < 128:
            theta = 3* (K+30)
        else:
            theta = 3 * (K+50)
        for i in range(len(pokemon_list)):
            sorted_pokemon1 = sorted(pokemon_list, key=lambda x: x.score, reverse=True)
            theta = 3*len((pokemon_list))-3-sorted_pokemon1[len(pokemon_list)+K-i].score if i > K else theta
            for j in range(i,len(pokemon_list)):
                if (i != j):
                    pokemon1 = pokemon_list[i]
                    pokemon2 = pokemon_list[j]
                    pokemon1_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                         pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                         pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type,
                                         pokemon1.skill2type, pokemon1.total_points)
                    pokemon2_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1,
                                         pokemon2.skill2, pokemon2.special_skill1, pokemon2.special_skill2,
                                         pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type,
                                         pokemon2.skill2type, pokemon2.total_points)
                    if (GGGG == 0):
                        pokemon1_1.useskill = pokemon1.useskill
                        pokemon2_2.useskill = pokemon2.useskill
                    result, result1, result_2 = None, None, None

                    if (int(damage_dict[pokemon1_1.name]['min_damage']) - int(
                            damage_dict[pokemon2_2.name]['max_damage']) > 3*pokemon2_2.health):
                        result = f"{pokemon1_1.name} 胜利"
                        count1 += 1
                    elif (int(damage_dict[pokemon2_2.name]['min_damage']) - int(
                            damage_dict[pokemon1_1.name]['max_damage']) > 3*pokemon1_1.health):
                        result = f"{pokemon2_2.name} 胜利"
                        count1 += 1
                    else:
                        result, result1, result_2 = battle(pokemon1_1, pokemon2_2, moshi, whe)
                    if result == f"{pokemon1_1.name} 胜利":
                        pokemon1.score -= 0  # pokemon1 获胜
                        pokemon2.score -= 3  # pokemon1 获胜
                        pokemon1.shuyinglist[0].append(pokemon2.name)
                        pokemon2.shuyinglist[2].append(pokemon1.name)
                        pokemon1.scorelist[0] += 1
                        pokemon2.scorelist[2] += 1
                    elif result == f"{pokemon2.name} 胜利":
                        pokemon1.score -= 3  # pokemon2 获胜
                        pokemon2.score -= 0  # pokemon2 获胜
                        pokemon1.shuyinglist[2].append(pokemon2.name)
                        pokemon2.shuyinglist[0].append(pokemon1.name)
                        pokemon1.scorelist[2] += 1
                        pokemon2.scorelist[0] += 1
                    else:
                        pokemon1.score -= 2  # 平局
                        pokemon2.score -= 2  # 平局
                        pokemon1.shuyinglist[1].append(pokemon2.name)
                        pokemon1.scorelist[1] += 1
                        pokemon2.shuyinglist[1].append(pokemon1.name)
                        pokemon2.scorelist[1] += 1
                    #shiqufenshu=pokemon1.scorelist[1]*2+pokemon1.scorelist[2]*3
                    shiqufenshu = 3*(len(pokemon_list)-1)-pokemon1.score
                    if(shiqufenshu>theta):
                        break
        print(count1)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"代码运行时间: {elapsed_time}秒")
    if(GGG==1):
        save_most_used_skill(pokemon_list, "most_used_skills.txt")
    return pokemon_list
def write_log(message):
    """将消息写入日志文件"""
    with open("log.txt", "a") as log_file:  # 以追加模式打开文件
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间
        log_file.write(f"{timestamp} - {message}\n")
class PokemonBattleApp:
    def __init__(self, root, pokemons,rank_system,useskilltable):
        self.root = root
        self.pokemons = pokemons
        self.rank_system=rank_system
        self.useskilltable=useskilltable
        self.selected_pokemon1 = None
        self.selected_pokemon2 = None
        self.selected_pokemon1_shuxing = None
        self.selected_pokemon2_shuxing = None
        self.lilian_pokemon = None
        self.lilian_pokemon_shuxing = None
        self.lilian_pokemon_list = None
        self.moshi=None
        self.moshi1 = None
        self.all_pokemon_list = [pokemon.name for pokemon in self.pokemons]
        self.pokemon_directory = './vision'  # 版本存储路径
        if not os.path.exists(self.pokemon_directory):
            os.makedirs(self.pokemon_directory)
        self.log_txt = 'log.txt'  # 版本存储路径
        self.whehter = "正常天气"
        self.team1 = []  # 队伍1
        self.team2 = []  # 队伍2
        self.team_size = 0  # 队伍成员数
        self.attribute_groups = self.group_pokemons_by_attribute()
        self.root.title("宝可梦对战系统")
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=100)
        self.battle_mode_label = tk.Label(self.main_frame, text="选择对战模式", font=("Arial", 16))
        self.battle_mode_label.pack(pady=20)
        self.single_battle_button = tk.Button(self.main_frame, text="单挑模式", command=self.open_single_battle,
                                              font=("Arial", 14), bg="#CC33CC", fg="white")
        self.single_battle_button.pack(pady=10)
        self.tournament_battle_button = tk.Button(self.main_frame, text="积分赛模式",
                                                  command=self.open_tournament_battle, font=("Arial", 14), bg="#994D00",
                                                  fg="white")
        self.tournament_battle_button.pack(pady=10)
        self.elimination_battle_button = tk.Button(self.main_frame, text="淘汰赛模式",
                                                   command=self.open_elimination_battle, font=("Arial", 14),
                                                   bg="#33664D", fg="white")
        self.elimination_battle_button.pack(pady=10)
        self.training_battle_button = tk.Button(self.main_frame, text="历练模式", command=self.training,
                                                font=("Arial", 14), bg="#AFCAAF", fg="white")
        self.training_battle_button.pack(pady=10)
        self.team_battle_button = tk.Button(self.main_frame, text="团体赛", command=self.open_team_battle,
                                            font=("Arial", 14), bg="#FF6347")
        self.team_battle_button.pack(pady=10)
        self.treasure_box_button = tk.Button(self.main_frame, text="百宝箱", command=self.open_treasure_box,
                                             font=("Arial", 14), bg="#FF9900", fg="white")
        self.treasure_box_button.pack(pady=10)
        self.ensure_log_file_exists()
        self.ALL_TEAM = []
        self.ALL_po = []
        self.attribute_battle_button = tk.Button(self.main_frame, text="属性大战",
                                                 command=self.show_feature_under_development,
                                                 font=("Arial", 14), bg="#FF6347", fg="white")
        self.attribute_battle_button.pack(pady=10)
        self.paiming_button = tk.Button(self.main_frame, text="排名",
                                                 command=self.paiming,
                                                 font=("Arial", 14), bg="#FF6347", fg="white")
        self.paiming_button.pack(pady=10)
        self.shijiesai_button = tk.Button(self.main_frame, text="世界赛",
                                        command=self.shijiesai,
                                        font=("Arial", 14), bg="#FE1339", fg="white")
        self.shijiesai_button.pack(pady=10)

    def shijiesai(self):
        self.main_frame.pack_forget()  # 隐藏主界面
        self.shijiesai_frame = tk.Frame(self.root)
        self.shijiesai_frame.pack(pady=20)

        # 返回按钮
        self.back_button = tk.Button(self.shijiesai_frame, text="返回", command=self.return_to_main_4, font=("Arial", 14))
        self.back_button.pack(pady=10)

        # 阶梯循环赛按钮
        self.ladder_button = tk.Button(self.shijiesai_frame, text="阶梯循环赛", command=self.show_under_development, font=("Arial", 14))
        self.ladder_button.pack(pady=10)

    def show_under_development(self):
        # 弹出提示框显示功能正在开发中
        messagebox.showinfo("提示", "该功能正在开发中")
    def paiming(self):
        self.main_frame.pack_forget()  # 隐藏主界面
        self.paiming_frame = tk.Frame(self.root)
        self.paiming_frame.pack(pady=20)
        self.back_button = tk.Button(self.paiming_frame, text="返回",
                                     command=self.return_to_main_3, font=("Arial", 14))
        self.back_button.pack(pady=10)
        self.entry_placeholder = "请输入宝可梦名称..."  # 占位符文本
        self.entry = tk.Entry(self.paiming_frame, fg="grey", font=("Arial", 12))
        self.entry.insert(0, self.entry_placeholder)
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.restore_placeholder)
        self.entry.bind('<KeyRelease>', self.update_suggestions)  # 监听输入事件
        self.entry.pack(pady=5)
        self.suggestion_box = tk.Listbox(self.paiming_frame, height=5, width=25)  # 控制显示的备选项数量
        self.suggestion_box.pack()
        self.suggestion_box.bind('<<ListboxSelect>>', self.fill_entry_from_listbox)
        self.pokemon_button = tk.Button(self.paiming_frame, text="查看宝可梦排名", command=self.show_pokemon_rank)
        self.pokemon_button.pack(pady=10)
        self.team_label = tk.Label(self.paiming_frame, text="选择团队类型", font=("Arial", 14))
        self.team_label.pack(pady=10)
        self.team_size_var = tk.StringVar(self.paiming_frame)
        self.team_size_var.set("2")  # 默认双人团队
        self.team_size_menu = tk.OptionMenu(self.paiming_frame, self.team_size_var, "2", "3", "5", "7")
        self.team_size_menu.pack(pady=5)
        self.entry_placeholder1 = "请输入团队名称:..."  # 占位符文本
        self.team_name_entry = tk.Entry(self.paiming_frame, fg="grey", font=("Arial", 12))
        self.team_name_entry.insert(0, self.entry_placeholder1)
        self.team_name_entry.bind("<FocusIn>", self.clear_placeholder1)
        self.team_name_entry.bind("<FocusOut>", self.restore_placeholder1)
        self.team_name_entry.bind('<KeyRelease>', self.update_suggestions1)  # 监听输入事件
        self.team_name_entry.pack(pady=5)
        self.suggestion_box1 = tk.Listbox(self.paiming_frame, height=5, width=25)  # 控制显示的备选项数量
        self.suggestion_box1.pack()
        self.suggestion_box1.bind('<<ListboxSelect>>', self.fill_entry_from_listbox1)
        self.team_button = tk.Button(self.paiming_frame, text="查看团队排名", command=self.show_team_rank)
        self.team_button.pack(pady=10)
        self.team_button1 = tk.Button(self.paiming_frame, text="查看全部个人排名", command=self.all_pokemon_rank)
        self.team_button1.pack(pady=10)
        self.team_button2 = tk.Button(self.paiming_frame, text="查看全部团队排名", command=self.all_team_rank)
        self.team_button2.pack(pady=10)
        self.result_text = tk.Text(self.paiming_frame, height=10, width=150)
        self.result_text.pack(pady=10)
    def all_pokemon_rank(self):
        COUNT = 1
        te=""
        for name, score in self.rank_system.pokemon_rankings.items():
            te+= f"{name} - 个人排名: { COUNT}- 得分: {score}\n"
            COUNT += 1
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, te)
    def all_team_rank(self):
        COUNT = 1
        te = ""
        team_size = int(self.team_size_var.get())
        rankings_dict =None
        if team_size == 2:
            rankings_dict = self.rank_system.team2_rankings
        elif team_size == 3:
            rankings_dict = self.rank_system.team3_rankings
        elif team_size == 5:
            rankings_dict = self.rank_system.team5_rankings
        elif team_size == 7:
            rankings_dict = self.rank_system.team7_rankings
        for name, score in rankings_dict.items():
            te += f"{name}  团队排名: {COUNT} 团队得分: {score.team_score} 成员: {score.namelist} \n"
            COUNT += 1
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, te)
    def show_pokemon_rank(self):
        pokemon_name =  self.entry.get()
        print(pokemon_name)
        rank,score = self.rank_system.get_pokemon_rank(pokemon_name)
        print( rank,score)
        if rank is not None:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"{pokemon_name} 的排名: {rank},分数为：{score}")
        else:
            messagebox.showerror("错误", f"没有找到宝可梦: {pokemon_name}")
    def show_team_rank(self):
        team_name = self.team_name_entry.get()
        team_size = int(self.team_size_var.get())
        team_rank,team = self.rank_system.get_team_rank(team_name, team_size)
        if team is not None:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END,
                                    f"{team.name} ，团队排名：{team_rank},团队得分为: {team.team_score} \n,团队成员为: {team.namelist}")
        else:
            messagebox.showerror("错误", f"没有找到团队: {team_name}")
    def shuju(self):
        attt = ["火", "水", "草", "电", "暗", "光", "力"]
        K = 7
        self.attribute_scores = {attr: 0 for attr in self.attributes.keys()}
        self.ALL_TEAM=[]
        self.ALL_po=[]
        for i in attt:
            pokemon_list = self.attribute_groups[i]
            jifen = round_robin_tournament(pokemon_list, K, "正常战斗模式", self.whehter)
            sorted_pokemons = sorted(jifen, key=self.ranking_key)
            selected_pokemon = sorted_pokemons[:K]
            self.ALL_TEAM.append(selected_pokemon)
        for i in self.ALL_TEAM:
            for j in i:
                self.ALL_po.append(j)
    def DT(self):
        try:
            random.shuffle(self.ALL_po)
            pokemons, bye_pokemons = self.handle_bye_pokemons(self.ALL_po)
            current_round_pokemons = pokemons
            all_rounds = []  # 用于存储每轮的对战信息
            round_number = 1
            while len(current_round_pokemons) > 1:
                num_matches = len(current_round_pokemons) // 2
                next_round_pokemons = []
                round_matches = []
                for i in range(0, len(current_round_pokemons), 2):
                    if i + 1 < len(current_round_pokemons):
                        flag = True
                        winname = None
                        winner = None
                        pokemon1 = current_round_pokemons[i]
                        pokemon2 = current_round_pokemons[i + 1]
                        if(round_number==3):
                            pokemon1.person_score += round_number**2
                            pokemon2.person_score += round_number ** 2
                            self.rank_system.update_pokemon_rank1(pokemon1)
                            self.rank_system.update_pokemon_rank1(pokemon2)
                            self.attribute_scores[pokemon1.attribute] += 1
                            self.attribute_scores[pokemon2.attribute] += 1
                        if (round_number == 4):
                            pokemon1.person_score += round_number ** 2
                            pokemon2.person_score += round_number ** 2
                            self.rank_system.update_pokemon_rank1(pokemon1)
                            self.rank_system.update_pokemon_rank1(pokemon2)
                            self.attribute_scores[pokemon1.attribute] += 2
                            self.attribute_scores[pokemon2.attribute] += 2
                        if (round_number == 5):
                            pokemon1.person_score += round_number ** 2
                            pokemon2.person_score += round_number ** 2
                            self.rank_system.update_pokemon_rank1(pokemon1)
                            self.rank_system.update_pokemon_rank1(pokemon2)
                            self.attribute_scores[pokemon1.attribute] += 3
                            self.attribute_scores[pokemon2.attribute] += 3
                        if (round_number == 6):
                            pokemon1.person_score += round_number ** 2
                            pokemon2.person_score += round_number ** 2
                            self.rank_system.update_pokemon_rank1(pokemon1)
                            self.rank_system.update_pokemon_rank1(pokemon2)
                            self.attribute_scores[pokemon1.attribute] += 4
                            self.attribute_scores[pokemon2.attribute] += 4
                        num = 1
                        while (flag):
                            pokemon1_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                                 pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                                 pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type,
                                                 pokemon1.skill2type, pokemon1.total_points)
                            pokemon2_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1,
                                                 pokemon2.skill2, pokemon2.special_skill1, pokemon2.special_skill2,
                                                 pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type,
                                                 pokemon2.skill2type, pokemon2.total_points)
                            winner_text, winner, result_3 = battle(pokemon1_1, pokemon2_2, self.moshi, self.whehter)
                            if winner_text == f"{pokemon1_1.name} 胜利":
                                flag = False
                                winname = pokemon1.name
                                winner = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                                 pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                                 pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type,
                                                 pokemon1.skill2type, pokemon1.total_points)
                            elif winner_text == f"{pokemon2_2.name} 胜利":
                                flag = False
                                winname = pokemon2.name
                                winner = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1, pokemon2.skill2, pokemon2.special_skill1, pokemon2.special_skill2,
                                                 pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type,
                                                 pokemon2.skill2type, pokemon2.total_points)
                            else:
                                flag = True
                                if (num > 5):
                                    flag = False
                                    options = [current_round_pokemons[i], current_round_pokemons[i + 1]]
                                    selected_option = random.choice(options)
                                    winname = selected_option.name
                                    winner = Pokemon(selected_option.name, selected_option.health,
                                                     selected_option.attribute, selected_option.skill1,
                                                     selected_option.skill2, selected_option.special_skill1,
                                                     selected_option.special_skill2,
                                                     selected_option.weaknesses, selected_option.resistances,
                                                     selected_option.skill1type,
                                                     selected_option.skill2type, selected_option.total_points)
                                num += 1
                        round_matches.append((pokemon1.name, pokemon2.name, winname))
                        next_round_pokemons.append(winner)
                if (round_number == 1):
                    for i in bye_pokemons:
                        pokemon1 = i
                        round_matches.append((pokemon1.name, "轮空", pokemon1.name))  # 轮空选手直接晋级
                        next_round_pokemons.append(pokemon1)
                all_rounds.append(round_matches)
                current_round_pokemons = next_round_pokemons
                round_number += 1
            winner = current_round_pokemons[0]
            winner.person_score += 49
            self.rank_system.update_pokemon_rank1(winner)
            save_rank_data(self.rank_system)
            self.rank_system.print_pokemon_rankings()
            self.attribute_scores[winner.attribute] += 4
            print("计算完成")
            round_num = 1
            text_content = "淘汰赛赛程：\n"
            for round_matches in all_rounds:
                aa = "    " * round_num
                print(aa)
                print(aa + f"第 {round_num} 轮:")
                bbb = aa + f"第 {round_num} 轮:"
                text_content += bbb + "\n"
                for match in round_matches:
                    pokemon1, pokemon2, winner = match
                    if pokemon2 != "轮空":
                        bbbb = aa + f"  {pokemon1} vs {pokemon2} -> {winner}"
                        text_content += bbbb + "\n"
                        print(aa + f"  {pokemon1} vs {pokemon2} -> {winner}")
                    else:
                        bbbb = aa + f"  {pokemon1} vs 轮空 -> {pokemon1} 晋级"
                        text_content += bbbb + "\n"
                        print(aa + f"  {pokemon1} vs 轮空 -> {pokemon1} 晋级")
                round_num += 1
            print("\n")
            print(self.attribute_scores)
            score_str = "\n".join([f"{attribute}: {score}" for attribute, score in self.attribute_scores.items()])
            messagebox.showinfo("单挑属性得分", score_str)
            write_log(text_content)
        except ValueError:
            messagebox.showerror("错误", "未进行数据准备！")
    def generate_team_name(self, team_type):
        """根据队伍类型自动生成队伍名称"""
        if team_type == 2:  # 双排队伍
            team_list = self.rank_system.team2_names
            team_prefix = "双排队伍"
        elif team_type == 3:  # 三排队伍
            team_list = self.rank_system.team3_names
            team_prefix = "三排队伍"
        elif team_type == 5:  # 五排队伍
            team_list = self.rank_system.team5_names
            team_prefix = "五排队伍"
        elif team_type == 7:  # 七排队伍
            team_list = self.rank_system.team7_names
            team_prefix = "七排队伍"
        else:
            raise ValueError("队伍类型错误")
        team_name = f"{team_prefix}{len(team_list) + 1}"
        team_list.append(team_name)  # 添加队伍名称到相应列表
        return team_name
    def SP(self):
        try:
            Team=[]
            for i in self.ALL_TEAM:
                team1 = T_EAM("name1", [i[0], i[1]])  # 2人团队
                team2 = T_EAM("name2", [i[2], i[3]])  # 2人团队
                namelist1=[i[0].name,i[1].name]
                namelist2 = [i[2].name, i[3].name]
                charu1=False
                charu2 = False
                for name, tea in self.rank_system.team2_rankings.items():
                    if(set(tea.namelist)==set(namelist1)):
                        team1.name=tea.name
                        charu1=True
                        team1.team_score = tea.team_score
                    if (set(tea.namelist) == set(namelist2)):
                        charu2 = True
                        team2.name = tea.name
                        team2.team_score = tea.team_score
                if(charu1==False):
                    team1.name = self.generate_team_name(len([i[0], i[1]]))
                    self.rank_system.add_team(team1,len(team1.members))
                if (charu2 == False):
                    team2.name=self.generate_team_name(len([i[2], i[3]]))
                    self.rank_system.add_team(team2, len(team2.members))
                Team.append(team1)
                Team.append(team2)
            random.shuffle(Team)
            next_Team=[]
            fuhuo=[]
            for i in range(0, len(Team), 2):
                team1 = Team[i]
                team2 = Team[i + 1]
                battle_result = self.team_battle(team1.members, team2.members)
                if(battle_result[-6:-1]=="队伍1获胜"):
                    next_Team.append(team1)
                    fuhuo.append(team2)
                else:
                    next_Team.append(team2)
                    fuhuo.append(team1)
            print("直接晋级队伍：")
            for i in  next_Team:
                print(i.members[0] .name,i.members[1].name)
            print("复活赛队伍：")
            for i in fuhuo:
                print(i.members[0].name, i.members[1].name)
            random.shuffle(fuhuo)
            team_temp=fuhuo[len(fuhuo)-1]
            fuhuo.pop()
            tt=1
            while(len(fuhuo)>=2):
                next_fuhuo=[]
                for i in range(0, len(fuhuo), 2):
                    team1 = fuhuo[i]
                    team2 = fuhuo[i + 1]
                    battle_result = self.team_battle(team1.members, team2.members)
                    if (battle_result[-6:-1] == "队伍1获胜"):
                        team2.team_score += 20
                        self.rank_system.update_team_rank(team2, len(team2.members))
                        next_fuhuo.append(team1)
                    else:
                        team1.team_score += 20
                        self.rank_system.update_team_rank(team1, len(team1.members))
                        next_fuhuo.append(team2)
                if(tt==1):
                    next_fuhuo.append(team_temp)
                    print("下一轮",len(next_fuhuo))
                fuhuo= next_fuhuo
                tt+=1
            print("复活赛晋级队伍：")
            print(fuhuo[0].members[0].name,fuhuo[0].members[1].name)
            next_Team.append(fuhuo[0])
            random.shuffle( next_Team)
            round_number=1
            while (len(next_Team) >= 2):
                next_fuhuo = []
                print("本轮参赛选手：")
                for i in next_Team:
                    print(i.members[0].name,i.members[1].name)
                for i in range(0, len(next_Team), 2):
                    team1 = next_Team[i]
                    team2 = next_Team[i + 1]
                    if (round_number == 1):
                        team1.team_score += 150
                        self.rank_system.update_team_rank(team1, len(team1.members))
                        team2.team_score += 150
                        self.rank_system.update_team_rank(team2, len(team2.members))
                        self.attribute_scores[team1.members[0].attribute] += 2
                        self.attribute_scores[team2.members[0].attribute] += 2
                    if (round_number == 2):
                        team1.team_score += 200
                        self.rank_system.update_team_rank(team1, len(team1.members))
                        team2.team_score += 200
                        self.rank_system.update_team_rank(team2, len(team2.members))
                        self.attribute_scores[team1.members[0].attribute] += 3
                        self.attribute_scores[team2.members[0].attribute] += 3
                    if (round_number == 3):
                        team1.team_score += 250
                        self.rank_system.update_team_rank(team1, len(team1.members))
                        team2.team_score += 250
                        self.rank_system.update_team_rank(team2, len(team2.members))
                        self.attribute_scores[team1.members[0].attribute] += 4
                        self.attribute_scores[team2.members[0].attribute] += 4
                    battle_result = self.team_battle(team1.members, team2.members)
                    if (battle_result[-6:-1] == "队伍1获胜"):
                        next_fuhuo.append(team1)
                    else:
                        next_fuhuo.append(team2)
                next_Team = next_fuhuo
                round_number +=1
            print("最终获胜队伍：")
            print(next_Team[0].members[0].name,next_Team[0].members[1].name)
            next_Team[0].team_score += 250
            self.rank_system.update_team_rank( next_Team[0], len(next_Team[0].members))
            self.attribute_scores[next_Team[0].members[0].attribute] += 4
            print(self.attribute_scores)
            score_str = "\n".join([f"{attribute}: {score}" for attribute, score in self.attribute_scores.items()])
            save_rank_data(self.rank_system)
            self.rank_system.print_team2_rankings()
            messagebox.showinfo("双排属性得分", score_str)
        except IndexError:
            messagebox.showerror("错误", "未进行数据准备！")
    def ShanP(self):
        try:
            Team = []
            for i in self.ALL_TEAM:
                team1 = T_EAM("name1", [i[0], i[1], i[2]])  # 2人团队
                namelist1 = [i[0].name, i[1].name, i[2].name]
                charu1 = False
                for name, tea in self.rank_system.team3_rankings.items():
                    if (set(tea.namelist) == set(namelist1)):
                        team1.name = tea.name
                        charu1 = True
                        team1.team_score = tea.team_score
                if (charu1 == False):
                    team1.name = self.generate_team_name(len([i[0], i[1], i[2]]))
                    self.rank_system.add_team(team1, len(team1.members))
                Team.append(team1)
            random.shuffle(Team)
            team_temp = Team[len(Team) - 1]
            Team.pop()
            tt = 1
            next_Team = []
            fuhuo = []
            for i in range(0, len(Team), 2):
                team1 = Team[i]
                team2 = Team[i + 1]
                battle_result = self.team_battle(team1.members, team2.members)
                if (battle_result[-6:-1] == "队伍1获胜"):
                    team1.team_score += 100
                    self.rank_system.update_team_rank(team1, len(team1.members))
                    next_Team.append(team1)
                    fuhuo.append(team2)
                else:
                    team2.team_score += 100
                    self.rank_system.update_team_rank(team2, len(team2.members))
                    next_Team.append(team2)
                    fuhuo.append(team1)
            print("直接晋级队伍：")
            for i in next_Team:
                print(i.members[0].name, i.members[1].name,i.members[2].name)
            print("复活赛队伍：")
            for i in fuhuo:
                print(i.members[0].name, i.members[1].name, i.members[2].name)
            print(team_temp.members[0].name, team_temp.members[1].name, team_temp.members[2].name)
            fuhuo.append( team_temp)
            taotai=[]
            while (len(fuhuo) >= 2):
                next_fuhuo = []
                for i in range(0, len(fuhuo), 2):
                    team1 = fuhuo[i]
                    team2 = fuhuo[i + 1]
                    battle_result = self.team_battle(team1.members, team2.members)
                    if (battle_result[-6:-1] == "队伍1获胜"):
                        team2.team_score += 30
                        self.rank_system.update_team_rank(team2, len(team2.members))
                        next_fuhuo.append(team1)
                        taotai.append(team2)
                    else:
                        team1.team_score += 30
                        self.rank_system.update_team_rank(team1, len(team1.members))
                        next_fuhuo.append(team2)
                        taotai.append(team1)
                fuhuo = next_fuhuo
            print("复活赛晋级队伍：")
            print(fuhuo[0].members[0].name, fuhuo[0].members[1].name,fuhuo[0].members[2].name)
            fuhuo[0].team_score += 100
            self.rank_system.update_team_rank(fuhuo[0], len(fuhuo[0].members))
            next_Team.append(fuhuo[0])
            random.shuffle(next_Team)
            for i in taotai:
                self.attribute_scores[i.members[0].attribute] += 2
            round_number = 1
            while (len(next_Team) >= 2):
                next_fuhuo = []
                print("本轮参赛选手：")
                for i in next_Team:
                    print(i.members[0].name, i.members[1].name,i.members[2].name)
                for i in range(0, len(next_Team), 2):
                    team1 = next_Team[i]
                    team2 = next_Team[i + 1]
                    if (round_number == 1):
                        self.attribute_scores[team1.members[0].attribute] += 3
                        self.attribute_scores[team2.members[0].attribute] += 3
                    if (round_number == 2):
                        self.attribute_scores[team1.members[0].attribute] += 4
                        self.attribute_scores[team2.members[0].attribute] += 4
                    battle_result = self.team_battle(team1.members, team2.members)
                    team1.team_score += 200
                    team2.team_score += 200
                    self.rank_system.update_team_rank(team1, len(team1.members))
                    self.rank_system.update_team_rank(team2, len(team2.members))
                    if (battle_result[-6:-1] == "队伍1获胜"):
                        next_fuhuo.append(team1)
                    else:
                        next_fuhuo.append(team2)
                next_Team = next_fuhuo
                round_number += 1
            print("最终获胜队伍：")
            print(next_Team[0].members[0].name, next_Team[0].members[1].name ,next_Team[0].members[2].name)
            next_Team[0].team_score += 300
            self.rank_system.update_team_rank(next_Team[0], len(next_Team[0].members))
            self.attribute_scores[next_Team[0].members[0].attribute] += 4
            print(self.attribute_scores)
            score_str = "\n".join([f"{attribute}: {score}" for attribute, score in self.attribute_scores.items()])
            save_rank_data(self.rank_system)
            self.rank_system.print_team3_rankings()
            messagebox.showinfo("三排属性得分", score_str)
        except IndexError:
            messagebox.showerror("错误", "未进行数据准备！")
    def WP(self):
        try:
            Team = []
            for i in self.ALL_TEAM:
                team1 = T_EAM("name1", [i[0], i[1], i[2], i[3], i[4]])  # 2人团队
                namelist1 = [i[0].name, i[1].name, i[2].name, i[3].name, i[4].name]
                charu1 = False
                for name, tea in self.rank_system.team5_rankings.items():
                    if (set(tea.namelist) == set(namelist1)):
                        team1.name = tea.name
                        charu1 = True
                        team1.team_score = tea.team_score
                if (charu1 == False):
                    team1.name = self.generate_team_name(len([i[0], i[1], i[2] ,i[3], i[4]]))
                    self.rank_system.add_team(team1, len(team1.members))
                Team.append(team1)
            random.shuffle(Team)
            team_temp = Team[len(Team) - 1]
            Team.pop()
            tt = 1
            next_Team = []
            fuhuo = []
            for i in range(0, len(Team), 2):
                team1 = Team[i]
                team2 = Team[i + 1]
                battle_result = self.team_battle(team1.members, team2.members)
                if (battle_result[-6:-1] == "队伍1获胜"):
                    team1.team_score += 150
                    self.rank_system.update_team_rank(team1, len(team1.members))
                    next_Team.append(team1)
                    fuhuo.append(team2)
                else:
                    team2.team_score += 150
                    self.rank_system.update_team_rank(team2, len(team2.members))
                    next_Team.append(team2)
                    fuhuo.append(team1)
            print("直接晋级队伍：")
            for i in next_Team:
                print(i.members[0].name, i.members[1].name, i.members[2].name, i.members[3].name, i.members[4].name)
            print("复活赛队伍：")
            for i in fuhuo:
                print(i.members[0].name, i.members[1].name, i.members[2].name, i.members[3].name, i.members[4].name)
            print(team_temp.members[0].name, team_temp.members[1].name, team_temp.members[2].name, team_temp.members[3].name, team_temp.members[4].name)
            fuhuo.append(team_temp)
            taotai = []
            while (len(fuhuo) >= 2):
                next_fuhuo = []
                for i in range(0, len(fuhuo), 2):
                    team1 = fuhuo[i]
                    team2 = fuhuo[i + 1]
                    battle_result = self.team_battle(team1.members, team2.members)
                    if (battle_result[-6:-1] == "队伍1获胜"):
                        team2.team_score += 50
                        self.rank_system.update_team_rank(team2, len(team2.members))
                        next_fuhuo.append(team1)
                        taotai.append(team2)
                    else:
                        team1.team_score += 50
                        self.rank_system.update_team_rank(team1, len(team1.members))
                        next_fuhuo.append(team2)
                        taotai.append(team1)
                fuhuo = next_fuhuo
            print("复活赛晋级队伍：")
            fuhuo[0].team_score += 150
            self.rank_system.update_team_rank(fuhuo[0], len(fuhuo[0].members))
            print(fuhuo[0].members[0].name, fuhuo[0].members[1].name, fuhuo[0].members[2].name, fuhuo[0].members[3].name, fuhuo[0].members[4].name)
            next_Team.append(fuhuo[0])
            random.shuffle(next_Team)
            for i in taotai:
                self.attribute_scores[i.members[0].attribute] += 3
            round_number = 1
            while (len(next_Team) >= 2):
                next_fuhuo = []
                print("本轮参赛选手：")
                for i in next_Team:
                    print(i.members[0].name, i.members[1].name, i.members[2].name, i.members[3].name, i.members[4].name)
                for i in range(0, len(next_Team), 2):
                    team1 = next_Team[i]
                    team2 = next_Team[i + 1]
                    if (round_number == 1):
                        team1.team_score += 250
                        self.rank_system.update_team_rank(team1, len(team1.members))
                        team2.team_score += 250
                        self.rank_system.update_team_rank(team2, len(team2.members))
                        self.attribute_scores[team1.members[0].attribute] += 4
                        self.attribute_scores[team2.members[0].attribute] += 4
                    if (round_number == 2):
                        team1.team_score += 350
                        self.rank_system.update_team_rank(team1, len(team1.members))
                        team2.team_score += 350
                        self.rank_system.update_team_rank(team2, len(team2.members))
                        self.attribute_scores[team1.members[0].attribute] += 5
                        self.attribute_scores[team2.members[0].attribute] += 5
                    battle_result = self.team_battle(team1.members, team2.members)
                    if (battle_result[-6:-1] == "队伍1获胜"):
                        next_fuhuo.append(team1)
                    else:
                        next_fuhuo.append(team2)
                next_Team = next_fuhuo
                round_number += 1
            print("最终获胜队伍：")
            print(next_Team[0].members[0].name, next_Team[0].members[1].name, next_Team[0].members[2].name,next_Team[0].members[3].name, next_Team[0].members[4].name)
            next_Team[0].team_score += 400
            self.rank_system.update_team_rank(next_Team[0], len(next_Team[0].members))
            save_rank_data(self.rank_system)
            self.rank_system.print_team5_rankings()
            self.attribute_scores[next_Team[0].members[0].attribute] += 5
            print(self.attribute_scores)
            score_str = "\n".join([f"{attribute}: {score}" for attribute, score in self.attribute_scores.items()])
            messagebox.showinfo("五排属性得分", score_str)
        except IndexError:
            messagebox.showerror("错误", "未进行数据准备！")
    def QP(self):
        try:
            Team = []
            for i in self.ALL_TEAM:
                team1 = T_EAM("name1", [i[0], i[1], i[2], i[3], i[4], i[5], i[6]])  # 2人团队
                namelist1 = [i[0].name, i[1].name, i[2].name, i[3].name, i[4].name, i[5].name, i[6].name]
                charu1 = False
                for name, tea in self.rank_system.team7_rankings.items():
                    if (set(tea.namelist) == set(namelist1)):
                        team1.name = tea.name
                        charu1 = True
                        team1.team_score = tea.team_score
                if (charu1 == False):
                    team1.name = self.generate_team_name(len([i[0], i[1], i[2], i[3], i[4], i[5], i[6]]))
                    self.rank_system.add_team(team1, len(team1.members))
                Team.append(team1)
            random.shuffle(Team)
            team_temp = Team[len(Team) - 1]
            Team.pop()
            tt = 1
            next_Team = []
            fuhuo = []
            for i in range(0, len(Team), 2):
                team1 = Team[i]
                team2 = Team[i + 1]
                battle_result = self.team_battle(team1.members, team2.members)
                if (battle_result[-6:-1] == "队伍1获胜"):
                    team1.team_score += 200
                    self.rank_system.update_team_rank(team1, len(team1.members))
                    next_Team.append(team1)
                    fuhuo.append(team2)
                else:
                    team2.team_score += 200
                    self.rank_system.update_team_rank(team2, len(team2.members))
                    next_Team.append(team2)
                    fuhuo.append(team1)
            print("直接晋级队伍：")
            for i in next_Team:
                print(i.members[0].name, i.members[1].name, i.members[2].name, i.members[3].name, i.members[4].name, i.members[5].name, i.members[6].name)
            print("复活赛队伍：")
            for i in fuhuo:
                print(i.members[0].name, i.members[1].name, i.members[2].name, i.members[3].name, i.members[4].name, i.members[5].name, i.members[6].name)
            print(team_temp.members[0].name, team_temp.members[1].name, team_temp.members[2].name, team_temp.members[3].name, team_temp.members[4].name, team_temp.members[5].name, team_temp.members[6].name)
            fuhuo.append(team_temp)
            taotai = []
            while (len(fuhuo) >= 2):
                next_fuhuo = []
                for i in range(0, len(fuhuo), 2):
                    team1 = fuhuo[i]
                    team2 = fuhuo[i + 1]
                    battle_result = self.team_battle(team1.members, team2.members)
                    if (battle_result[-6:-1] == "队伍1获胜"):
                        team2.team_score += 70
                        self.rank_system.update_team_rank(team2, len(team2.members))
                        next_fuhuo.append(team1)
                        taotai.append(team2)
                    else:
                        team1.team_score += 70
                        self.rank_system.update_team_rank(team1, len(team1.members))
                        next_fuhuo.append(team2)
                        taotai.append(team1)
                fuhuo = next_fuhuo
            print("复活赛晋级队伍：")
            print(fuhuo[0].members[0].name, fuhuo[0].members[1].name, fuhuo[0].members[2].name, fuhuo[0].members[3].name, fuhuo[0].members[4].name, fuhuo[0].members[5].name, fuhuo[0].members[6].name)
            fuhuo[0].team_score += 200
            self.rank_system.update_team_rank(fuhuo[0], len(fuhuo[0].members))
            next_Team.append(fuhuo[0])
            random.shuffle(next_Team)
            for i in taotai:
                self.attribute_scores[i.members[0].attribute] += 4
            round_number = 1
            while (len(next_Team) >= 2):
                next_fuhuo = []
                print("本轮参赛选手：")
                for i in next_Team:
                    print(i.members[0].name, i.members[1].name, i.members[2].name, i.members[3].name, i.members[4].name, i.members[5].name, i.members[6].name)
                for i in range(0, len(next_Team), 2):
                    team1 = next_Team[i]
                    team2 = next_Team[i + 1]
                    if (round_number == 1):
                        team1.team_score += 300
                        self.rank_system.update_team_rank(team1, len(team1.members))
                        team2.team_score += 300
                        self.rank_system.update_team_rank(team2, len(team2.members))
                        self.attribute_scores[team1.members[0].attribute] += 5
                        self.attribute_scores[team2.members[0].attribute] += 5
                    if (round_number == 2):
                        team1.team_score += 400
                        self.rank_system.update_team_rank(team1, len(team1.members))
                        team2.team_score += 400
                        self.rank_system.update_team_rank(team2, len(team2.members))
                        self.attribute_scores[team1.members[0].attribute] += 7
                        self.attribute_scores[team2.members[0].attribute] += 7
                    battle_result = self.team_battle(team1.members, team2.members)
                    if (battle_result[-6:-1] == "队伍1获胜"):
                        next_fuhuo.append(team1)
                    else:
                        next_fuhuo.append(team2)
                next_Team = next_fuhuo
                round_number += 1
            print("最终获胜队伍：")
            print(next_Team[0].members[0].name, next_Team[0].members[1].name, next_Team[0].members[2].name, next_Team[0].members[3].name,
                  next_Team[0].members[4].name, next_Team[0].members[5].name,
                  next_Team[0].members[6].name)
            next_Team[0].team_score += 300
            self.rank_system.update_team_rank(next_Team[0], len(next_Team[0].members))
            self.attribute_scores[next_Team[0].members[0].attribute] += 7
            save_rank_data(self.rank_system)
            self.rank_system.print_team7_rankings()
            print(self.attribute_scores)
            score_str = "\n".join([f"{attribute}: {score}" for attribute, score in self.attribute_scores.items()])
            messagebox.showinfo("七排属性得分", score_str)
        except IndexError:
            messagebox.showerror("错误", "未进行数据准备！")
    def auto(self):
        self.DT()
        self.SP()
        self.ShanP()
        self.WP()
        self.QP()
    def qingkong(self):
        self.attribute_scores = {attr: 0 for attr in self.attributes.keys()}
    def JFCK(self):
        score_str = "\n".join([f"{attribute}: {score}" for attribute, score in self.attribute_scores.items()])
        messagebox.showinfo("当前属性得分", score_str)
    def show_feature_under_development(self):
        """弹出窗口，显示功能开发中的信息"""
        self.main_frame.pack_forget()  # 隐藏主界面
        self.whehter = "正常天气"
        self.feature_battle_frame = tk.Frame(self.root)
        self.feature_battle_frame.pack(pady=20)
        self.weather_var = tk.StringVar(value="正常天气")  # 默认天气为晴天
        self.attributes = {attr: [] for attr in ["火", "水", "草", "电", "暗", "光", "力"]}
        self.attribute_scores = {attr: 0 for attr in self.attributes.keys()}
        print(self.attribute_scores)
        self.weather_menu = tk.OptionMenu(
            self.feature_battle_frame,
            self.weather_var,  # 绑定天气变量
            "正常天气", "重力太空", "极热沙漠", "暗黑界域", "海洋之星", "藤蔓之眼", "光明城堡", "雷霆风暴", "众生平等",
            command=self.on_weather_change  # 回调函数
        )
        self.weather_menu.grid(row=0, column=0, padx=10, pady=10)
        self.back_button = tk.Button(self.feature_battle_frame, text="返回",
                                     command=self.return_to_main_2, font=("Arial", 14))
        self.back_button.grid(row=0, column=2, padx=10, pady=15, sticky="w")
        self.zhunbei_button = tk.Button(self.feature_battle_frame, text="数据准备",
                                     command=self.shuju, font=("Arial", 14))
        self.zhunbei_button.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        self.DT_button = tk.Button(self.feature_battle_frame, text="属性单挑",
                                        command=self.DT, font=("Arial", 14))
        self.DT_button.grid(row=1, column=0, padx=10, pady=15, sticky="w")
        self.SP_button = tk.Button(self.feature_battle_frame, text="属性双排挑战赛",
                                   command=self.SP, font=("Arial", 14))
        self.SP_button.grid(row=1, column=1, padx=10, pady=15, sticky="w")
        self.shan_button = tk.Button(self.feature_battle_frame, text="属性三排挑战赛",
                                   command=self.ShanP, font=("Arial", 14))
        self.shan_button.grid(row=1, column=2, padx=10, pady=15, sticky="w")
        self.wu_button = tk.Button(self.feature_battle_frame, text="属性五排挑战赛",
                                     command=self.WP, font=("Arial", 14))
        self.wu_button.grid(row=2, column=0, padx=10, pady=15, sticky="w")
        self.Q_button = tk.Button(self.feature_battle_frame, text="属性七排挑战赛",
                                   command=self.QP, font=("Arial", 14))
        self.Q_button.grid(row=2, column=1, padx=10, pady=15, sticky="w")
        self.AUTO_button = tk.Button(self.feature_battle_frame, text="全自动挑战赛",
                                  command=self.auto, font=("Arial", 14))
        self.AUTO_button.grid(row=2, column=2, padx=10, pady=15, sticky="w")
        self.qing_button = tk.Button(self.feature_battle_frame, text="积分重置",
                                     command=self.qingkong, font=("Arial", 14))
        self.qing_button.grid(row=3, column=0, padx=10, pady=15, sticky="w")
        self.qing_button1 = tk.Button(self.feature_battle_frame, text="积分查看",
                                     command=self.JFCK, font=("Arial", 14))
        self.qing_button1.grid(row=3, column=2, padx=10, pady=15, sticky="w")
    def open_team_battle(self):
        """打开团体赛界面"""
        self.main_frame.pack_forget()  # 隐藏主界面
        self.team_battle_frame = tk.Frame(self.root)
        self.team_battle_frame.pack(pady=20)
        self.whehter = "正常天气"
        write_log("进入团体赛模式")
        self.weather_var = tk.StringVar(value="正常天气")  # 默认天气为晴天
        self.weather_menu = tk.OptionMenu(
            self.team_battle_frame,
            self.weather_var,  # 绑定天气变量
            "正常天气", "重力太空", "极热沙漠", "暗黑界域", "海洋之星", "藤蔓之眼", "光明城堡", "雷霆风暴", "众生平等",
            command=self.on_weather_change  # 回调函数
        )
        self.weather_menu.grid(row=0, column=0, padx=10, pady=10)
        self.back_button = tk.Button(self.team_battle_frame, text="返回", command=self.return_to_mainq,
                                     font=("Arial", 14))
        self.back_button.grid(row=0, column=1, padx=10, pady=15)
        self.team_size_label = tk.Label(self.team_battle_frame, text="每队成员数: ", font=("Arial", 12))
        self.team_size_label.grid(row=1, column=0, padx=10, pady=10)
        self.team_size_entry = tk.Entry(self.team_battle_frame, width=10)
        self.team_size_entry.grid(row=1, column=1, padx=10, pady=10)
        self.set_team_size_button = tk.Button(self.team_battle_frame, text="设置队伍人数", command=self.set_team_size)
        self.set_team_size_button.grid(row=1, column=2, padx=10, pady=10)
    def return_to_mainq(self):
        """返回主界面"""
        self.team_battle_frame.pack_forget()  # 隐藏团体赛界面
        self.main_frame.pack(pady=20)  # 显示主界面
    def set_team_size(self):
        """设置队伍的成员数"""
        try:
            self.team_size = int(self.team_size_entry.get())
            if self.team_size < 1:
                raise ValueError("成员数必须大于0")
            self.team1 = []
            self.team2 = []
            write_log(f"设置队伍成员数为：{self.team_size}")
            self.setup_team_battle()
        except ValueError:
            messagebox.showwarning("无效输入", "请输入一个有效的队伍成员数")
    def setup_team_battle(self):
        """设置团队对战界面，显示两队选择宝可梦的界面"""
        self.attribute_label_training = tk.Label(self.team_battle_frame, text="选择属性进行团体赛",
                                                 font=("Arial", 14))
        self.attribute_label_training.grid(row=2, column=0, padx=10, pady=10)
        self.attribute_listbox_training = tk.Listbox(self.team_battle_frame, height=6, width=20,
                                                     selectmode=tk.SINGLE)
        self.attribute_listbox_training.grid(row=3, column=0, padx=10, pady=10)
        training_attributes = ['力', '电', '水', '火', '光', '暗', '草', '全体']  # 添加属性选项
        for attribute in training_attributes:
            self.attribute_listbox_training.insert(tk.END, attribute)
        self.attribute_listbox_training.bind("<<ListboxSelect>>", self.update_pok_list)
        self.team1_label = tk.Label(self.team_battle_frame, text="队伍1宝可梦", font=("Arial", 12))
        self.team1_label.grid(row=2, column=1, padx=10, pady=10)
        self.team1_listbox = tk.Listbox(self.team_battle_frame, height=6, width=20)
        self.team1_listbox.grid(row=3, column=1, padx=10, pady=10)
        self.team2_label = tk.Label(self.team_battle_frame, text="队伍2宝可梦", font=("Arial", 12))
        self.team2_label.grid(row=2, column=2, padx=10, pady=10)
        self.team2_listbox = tk.Listbox(self.team_battle_frame, height=6, width=20)
        self.team2_listbox.grid(row=3, column=2, padx=10, pady=10)
        self.delete_pkm1 = None
        self.delete_pkm2 = None
        self.list = None
        self.team1_listbox.bind("<<ListboxSelect>>", self.update_pokemon1)
        self.team2_listbox.bind("<<ListboxSelect>>", self.update_pokemon2)
        self.add_from_score_button = tk.Button(self.team_battle_frame, text="积分赛添加到队伍一",
                                               command=self.add_from_score)
        self.add_from_score_button.grid(row=5, column=0, padx=10, pady=10)
        self.add1_from_score_button = tk.Button(self.team_battle_frame, text="积分赛添加到队伍二",
                                                command=self.add_from_score1)
        self.add1_from_score_button.grid(row=6, column=0, padx=10, pady=10)
        self.pokemon_listbox = tk.Listbox(self.team_battle_frame, height=6, width=20)
        self.pokemon_listbox.grid(row=4, column=0, padx=10, pady=10)
        self.add1_selected_pokemon_button = tk.Button(self.team_battle_frame, text="添加宝可梦到队伍1",
                                                      command=lambda: self.add_pokemon_to_team(self.team1))
        self.add1_selected_pokemon_button.grid(row=4, column=1, padx=10, pady=10)
        self.add2_selected_pokemon_button = tk.Button(self.team_battle_frame, text="添加宝可梦到队伍2",
                                                      command=lambda: self.add_pokemon_to_team(self.team2))
        self.add2_selected_pokemon_button.grid(row=4, column=2, padx=10, pady=10)
        self.delete1_selected_pokemon_button = tk.Button(self.team_battle_frame, text="删除队伍1宝可梦",
                                                         command=self.delete_pokemon_to_team1)
        self.delete1_selected_pokemon_button.grid(row=5, column=1, padx=10, pady=10)
        self.delete2_selected_pokemon_button = tk.Button(self.team_battle_frame, text="删除队伍2宝可梦",
                                                         command=self.delete_pokemon_to_team2)
        self.delete2_selected_pokemon_button.grid(row=5, column=2, padx=10, pady=10)
        self.tema_button = tk.Button(self.team_battle_frame, text="开始团体对战",
                                     command=self.tema_battle)
        self.tema_button.grid(row=0, column=2, padx=10, pady=10)
        self.result_text = tk.Text(self.team_battle_frame, height=10, width=60, wrap=tk.WORD)
        self.result_text.grid(row=6, column=1, columnspan=3, padx=10, pady=10)
    def tema_battle(self):
        print("开始团队对战")
        battle_result = self.team_battle(self.team1, self.team2)
        self.result_text.delete(1.0, tk.END)  # 清空文本框
        self.result_text.insert(tk.END, battle_result)  # 插入战斗日志
    def team_battle(self,team1, team2):
        team_1=[]
        team_2 = []
        for pokemon1 in team1:
            pokemon1_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                 pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                 pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type,
                                 pokemon1.skill2type, pokemon1.total_points)
            team_1.append(pokemon1_1)
        for pokemon1 in team2:
            pokemon1_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                 pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                 pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type,
                                 pokemon1.skill2type, pokemon1.total_points)
            team_2.append(pokemon1_1)
        """模拟团队对战"""
        battle_log = []  # 用来记录每次战斗的结果
        team_1_health = [pokemon.health for pokemon in team_1]  # 每个宝可梦的初始生命值
        team_2_health = [pokemon.health for pokemon in team_2]
        battle_round = 1
        while team_1 and team_2:
            battle_log.append(f"回合 {battle_round}:")
            pokemon1 = team_1[0]
            pokemon2 = team_2[0]
            result,r2,result_2  = battle(pokemon1, pokemon2,"正常战斗模式",self.whehter)  # 假设battle函数返回结果：例如 "宝可梦A 胜利" 或 "平局"
            if (result == f"{pokemon1.name} 胜利")and(result_2 == "1"):
                battle_log.append(f"{pokemon1.name} 胜利！,击败了队伍2的 {pokemon2.name}")
                team_1_health[0] = pokemon1.health  # 保持战斗结束时的生命值
                team_1[0].health=pokemon1.health
                team_2.pop(0)
                if team_2_health:
                    team_2_health.pop(0)
                else:
                    print("队伍2的生命值列表已空，无法继续战斗！")
            elif (result == f"{pokemon2.name} 胜利")and(result_2 == "2"):
                battle_log.append(f"{pokemon2.name} 胜利！,击败了队伍1的 {pokemon1.name}")
                team_2_health[0] = pokemon2.health  # 保持战斗结束时的生命值
                team_2[0].health = pokemon2.health
                team_1.pop(0)
                if team_1_health:
                    team_1_health.pop(0)
                else:
                    print("队伍1的生命值列表已空，无法继续战斗！")
            else:
                battle_log.append("平局！,将两个宝可梦放至队伍尾部")
                team_1.pop(0)
                team_2.pop(0)
                pokemon1_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                     pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                     pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type,
                                     pokemon1.skill2type, pokemon1.total_points)
                pokemon2_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1,
                                     pokemon2.skill2, pokemon2.special_skill1, pokemon2.special_skill2,
                                     pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type,
                                     pokemon2.skill2type, pokemon2.total_points)
                team_1.append(pokemon1_1)
                team_2.append(pokemon2_2)
                if team_1_health:
                    team_1_health.pop(0)
                if team_2_health:
                    team_2_health.pop(0)
            battle_round += 1  # 下一回合
        if len(team_1) == 0:
            battle_log.append("队伍2获胜！")
        elif len(team_2) == 0:
            battle_log.append("队伍1获胜！")
        return "\n".join(battle_log)
    def update_pok_list(self, event):
        """根据选择的属性，更新宝可梦列表"""
        selected_index = self.attribute_listbox_training.curselection()
        if not selected_index:
            messagebox.showwarning("属性未选择", "未选择宝可梦的属性")
            return
        selected_attribute = self.attribute_listbox_training.get(selected_index)
        available_pokemons = [pokemon for pokemon in self.pokemons if pokemon.attribute == selected_attribute]
        self.list = available_pokemons
        if available_pokemons:
            self.pokemon_listbox.delete(0, tk.END)  # 清空列表
            for pokemon in available_pokemons:
                self.pokemon_listbox.insert(tk.END, pokemon.name)
    def update_pokemon1(self, event):
        selected_index = self.team1_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("队伍一宝可梦未选择", "未选择队伍一的宝可梦")
            return
        self.delete_pkm1 = self.team1[selected_index[0]]
        print(self.delete_pkm1)
    def update_pokemon2(self, event):
        selected_index = self.team2_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("队伍二宝可梦未选择", "未选择队伍二的宝可梦")
            return
        self.delete_pkm2 = self.team2[selected_index[0]]
        print(self.delete_pkm2)
    def add_from_score(self):
        """从积分赛中选择宝可梦并加入队伍"""
        selected_index = self.attribute_listbox_training.curselection()
        if not selected_index:
            messagebox.showwarning("属性未选择", "未选择宝可梦的属性")
            return
        selected_attribute = self.attribute_listbox_training.get(selected_index)
        if (selected_attribute == '全体'):
            pokemon_list = self.pokemons
        else:
            pokemon_list = self.attribute_groups[selected_attribute]
        jifen = round_robin_tournament(pokemon_list, self.team_size, "正常战斗模式",self.whehter)
        sorted_pokemons = sorted(jifen, key=self.ranking_key)
        selected_pokemon = sorted_pokemons[:self.team_size]
        selected_pokemon.reverse()
        self.team1 = selected_pokemon
        self.update_team_display()
    def add_from_score1(self):
        """从积分赛中选择宝可梦并加入队伍"""
        selected_index = self.attribute_listbox_training.curselection()
        if not selected_index:
            messagebox.showwarning("属性未选择", "未选择宝可梦的属性")
            return
        selected_attribute = self.attribute_listbox_training.get(selected_index)
        if (selected_attribute == '全体'):
            pokemon_list = self.pokemons
        else:
            pokemon_list = self.attribute_groups[selected_attribute]
        jifen = round_robin_tournament(pokemon_list, self.team_size, "正常战斗模式",self.whehter)
        sorted_pokemons = sorted(jifen, key=self.ranking_key)
        selected_pokemon = sorted_pokemons[:self.team_size]
        selected_pokemon.reverse()
        self.team2 = selected_pokemon
        self.update_team_display()
    def add_pokemon_to_team(self, team):
        """将选中的宝可梦添加到指定队伍"""
        if len(team) >= self.team_size:
            messagebox.showwarning("队伍已满", "该队伍已达到最大成员数")
            return
        selected_index = self.pokemon_listbox.curselection()
        if selected_index:
            selected_pokemon = self.list[selected_index[0]]
            team.append(selected_pokemon)
            self.update_team_display()
    def delete_pokemon_to_team1(self):
        if self.delete_pkm1:
            gen_pokemons = [pokemon for pokemon in self.team1 if pokemon.name != self.delete_pkm1.name]
            self.team1 = gen_pokemons
            self.update_team_display()
    def delete_pokemon_to_team2(self):
        if self.delete_pkm2:
            gen_pokemons = [pokemon for pokemon in self.team2 if pokemon.name != self.delete_pkm2.name]
            self.team2 = gen_pokemons
            self.update_team_display()
    def update_team_display(self):
        """更新队伍宝可梦显示"""
        self.team1_listbox.delete(0, tk.END)
        a="队伍一宝可梦有："
        for pokemon in self.team1:
            a +=pokemon.name
            a+=", "
            self.team1_listbox.insert(tk.END, pokemon.name)
        write_log(a)
        self.team2_listbox.delete(0, tk.END)
        b = "队伍二宝可梦有："
        for pokemon in self.team2:
            b += pokemon.name
            b += ", "
            self.team2_listbox.insert(tk.END, pokemon.name)
        write_log(b)
    def ensure_log_file_exists(self):
        """确保日志文件存在，如果不存在则创建它"""
        if not os.path.exists(self.log_txt):
            with open(self.log_txt, 'w') as f:
                f.write('日志文件创建于：' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
            print(f"{self.log_txt} 文件已创建。")
    def open_treasure_box(self):
        write_log("打开百宝箱界面")
        self.main_frame.pack_forget()  # 隐藏主界面
        self.bai_frame = tk.Frame(self.root)
        self.bai_frame.pack(pady=20)
        self.query_button = tk.Button(self.bai_frame, text="查询宝可梦", command=self.query_pokemon,
                                 font=("Arial", 12), bg="#00BFFF")
        self.query_button.grid(row=0, column=0, padx=20, pady=10)
        self.add_button = tk.Button(self.bai_frame, text="增加宝可梦", command=self.add_pokemon,
                               font=("Arial", 12), bg="#32CD32")
        self.add_button.grid(row=1, column=0, padx=20, pady=10)
        self.modify_button = tk.Button(self.bai_frame, text="修改宝可梦", command=self.modify_pokemon,
                                  font=("Arial", 12), bg="#FFD700")
        self.modify_button.grid(row=2, column=0, padx=20, pady=10)
        self.delete_button = tk.Button(self.bai_frame, text="删除宝可梦", command=self.delete_pokemon,
                                  font=("Arial", 12), bg="#FF6347")
        self.delete_button.grid(row=3, column=0, padx=20, pady=10)
        self.version_control_button = tk.Button(self.bai_frame, text="版本控制", command=self.version_control,
                                           font=("Arial", 12), bg="#8A2BE2")
        self.version_control_button.grid(row=4, column=0, padx=20, pady=10)
        self.view_log_button = tk.Button(self.bai_frame, text="日志功能", command=self.view_log,
                                    font=("Arial", 12), bg="#DC143C")
        self.view_log_button.grid(row=5, column=0, padx=20, pady=10)
        self.back_button = tk.Button(self.bai_frame, text="返回主界面", command=self.return_to_mainn,
                                font=("Arial", 12), bg="#A9A9A9")
        self.back_button.grid(row=6, column=0, padx=20, pady=10)
    def query_pokemon(self):
        print("查询宝可梦")
        write_log('打开查询宝可梦功能')
        query_window = tk.Toplevel(self.root)
        query_window.title("查询宝可梦")
        result_listbox = Listbox(query_window, height=10, width=50)
        result_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        def populate_listbox(listbox):
            """初始化宝可梦列表框，将所有宝可梦添加到列表中"""
            listbox.delete(0, 'end')  # 清空列表框
            for pokemon in self.pokemons:
                listbox.insert('end', pokemon.name)  # 将宝可梦名称添加到列表框中
        populate_listbox(result_listbox)
        Label(query_window, text="请输入宝可梦名称:").grid(row=0, column=0, padx=5, pady=5)
        search_entry = Entry(query_window, width=30)
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        details_label = Label(query_window, text="宝可梦详细信息将显示在这里", justify="left")
        details_label.grid(row=2, column=0, columnspan=3, padx=5, pady=10)
        def perform_query():
            Q_name =  search_entry.get()
            try:
                print( Q_name )
                write_log(f"查询了： {Q_name} 的信息")
                selected_pokemon = [pokemon for pokemon in self.pokemons if pokemon.name == Q_name][0]
                details_label.config(text="")  # 清空显示的宝可梦详情
                if selected_pokemon:
                    details=""  # 清空显示的宝可梦详情
                    s1 = f"名称: {selected_pokemon.name}  属性： {selected_pokemon.attribute}  HP： {selected_pokemon.health}  弱点： {selected_pokemon.weaknesses[0]}  抵抗： {selected_pokemon.resistances[0]}\n"
                    s2 = f"技能1伤害：{selected_pokemon.skill1[0]}  技能1消耗：{selected_pokemon.skill1[1]}  技能2伤害：{selected_pokemon.skill2[0]} 技能2消耗：{selected_pokemon.skill2[1]}\n"
                    s3 = f"特殊技能1：{selected_pokemon.special_skill1}  特殊技能2：{selected_pokemon.special_skill2} \n"
                    details+=s1
                    details+=s2
                    details += s3
                    details_label.config(text=details)
                else:
                    details_label.config(text="未找到该宝可梦的详细信息。")
            except IndexError:
                messagebox.showwarning("宝可梦不存在", "请选择一个宝可梦进行查询！")
        def update_suggestions(event=None):
            query = search_entry.get() # 获取输入内容并转换为小写
            result_listbox.delete(0, END)  # 清空 Listbox
            if query.strip():  # 非空查询
                best_matches = process.extract(query, self.all_pokemon_list, limit=10)  # 返回最相关的5个
                for match in best_matches:
                    result_listbox.insert(tk.END,
                                               match[0] + "    (相似度): " + str(match[1]) + "%")  # 将匹配结果加入 Listbox
        def fill_entry_from_listbox(event):
            selected_index = result_listbox.curselection()
            if selected_index:
                selected_value = result_listbox.get(selected_index)
                pokemon_name = selected_value.split("    (相似度): ")[0]  # 提取 "相似度" 前面的名称部分
                search_entry.delete(0, END)  # 清空输入框
                search_entry.insert(0, pokemon_name)  # 填入选中的名称
                update_suggestions(None)
                perform_query()
        query_button = Button(query_window, text="查询", command=perform_query)
        query_button.grid(row=0, column=2, padx=5, pady=5)
        search_entry.bind('<KeyRelease>', update_suggestions)  # 键盘释放时更新候选项
        result_listbox.bind('<<ListboxSelect>>', fill_entry_from_listbox)  # 点击 Listbox 项填入输入框
        Button(query_window, text="关闭", command=query_window.destroy).grid(row=3, column=1, pady=10)
    def add_pokemon(self):
        write_log('打开新增宝可梦功能')
        print("增加宝可梦")
        add_window = Toplevel(self.root)
        add_window.title("新增宝可梦")
        Label(add_window, text="名称:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = Entry(add_window, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        Label(add_window, text="HP:").grid(row=1, column=0, padx=5, pady=5)
        HP_entry = Entry(add_window, width=30)
        HP_entry.grid(row=1, column=1, padx=5, pady=5)
        Label(add_window, text="属性:").grid(row=2, column=0, padx=5, pady=5)
        attribute_options = ['光','水', '火','暗','草', '电', '力']  # 特殊技能列表
        attribute_var = StringVar()
        attribute_var.set( attribute_options[0])  # 默认选择第一个特殊技能
        attribute_menu = OptionMenu(add_window,  attribute_var, * attribute_options)
        attribute_menu.grid(row=2, column=1, padx=5, pady=5)
        Label(add_window, text="弱点 :").grid(row=3, column=0, padx=5, pady=5)
        weaknesses_options = ["力", "光", "暗", "火", "草", "水", "电", "无" ]  # 特殊技能列表
        weaknesses_var = StringVar()
        weaknesses_var.set(weaknesses_options[0])  # 默认选择第一个特殊技能
        weaknesses_menu = OptionMenu(add_window, weaknesses_var, *weaknesses_options)
        weaknesses_menu.grid(row=3, column=1, padx=5, pady=5)
        Label(add_window, text="抵抗  ：").grid(row=4, column=0, padx=5, pady=5)
        resistances_options = ["力", "光", "暗", "火", "草", "水", "电", "无", "全"]  # 特殊技能列表
        resistances_var = StringVar()
        resistances_var.set(resistances_options[0])  # 默认选择第一个特殊技能
        resistances_menu = OptionMenu(add_window, resistances_var, *resistances_options)
        resistances_menu.grid(row=4, column=1, padx=5, pady=5)
        Label(add_window, text="技能1伤害:").grid(row=5, column=0, padx=5, pady=5)
        skill1_damage_entry = Entry(add_window, width=30)
        skill1_damage_entry.grid(row=5, column=1, padx=5, pady=5)
        cost_options = ['1', '2', '3','4']  # 特殊技能列表
        Label(add_window, text="技能1消耗点数 (1-4):").grid(row=6, column=0, padx=5, pady=5)
        skill1_cost_var = StringVar()
        skill1_cost_var.set( cost_options[0])  # 默认选择第一个特殊技能
        skill1_cost_menu = OptionMenu(add_window,  skill1_cost_var, * cost_options)
        skill1_cost_menu.grid(row=6 ,column=1, padx=5, pady=5)
        Label(add_window, text="技能2伤害:").grid(row=7, column=0, padx=5, pady=5)
        skill2_damage_entry = Entry(add_window, width=30)
        skill2_damage_entry.grid(row=7, column=1, padx=5, pady=5)
        Label(add_window, text="技能2消耗 (1-4):").grid(row=8, column=0, padx=5, pady=5)
        skill2_cost_var = StringVar()
        skill2_cost_var.set(cost_options[0])  # 默认选择第一个特殊技能
        skill2_cost_menu = OptionMenu(add_window, skill2_cost_var, *cost_options)
        skill2_cost_menu.grid(row=8, column=1, padx=5, pady=5)
        Label(add_window, text="特殊技能1:").grid(row=9, column=0, padx=5, pady=5)
        special_skill1_options = ["无","盾牌", "反射伤害", "急速攻击", "治疗", "燃烧", "克制"] # 特殊技能列表
        special_skill1_var = StringVar()
        special_skill1_var.set(special_skill1_options[0])  # 默认选择第一个特殊技能
        special_skill1_menu = OptionMenu(add_window, special_skill1_var, *special_skill1_options)
        special_skill1_menu.grid(row=9, column=1, padx=5, pady=5)
        Label(add_window, text="特殊技能2:").grid(row=10, column=0, padx=5, pady=5)
        special_skill2_var = StringVar()
        special_skill2_var.set(special_skill1_options[0])  # 默认选择第一个特殊技能
        special_skill2_menu = OptionMenu(add_window, special_skill2_var, *special_skill1_options)
        special_skill2_menu.grid(row=10, column=1, padx=5, pady=5)
        def save_pokemon():
            name = name_entry.get()
            attribute = attribute_var.get()
            t1=attribute
            t1+="·"+name
            name=t1
            if any(pokemon.name == name for pokemon in self.pokemons):
                messagebox.showwarning("名称已存在", "该宝可梦名称已存在，请选择一个不同的名称。")
            else:
                attribute = attribute_var.get()
                weaknesses = weaknesses_var.get()  # 使用逗号分隔多个弱点
                resistances = resistances_var.get()  # 使用逗号分隔多个抵抗
                HP=HP_entry.get()
                skill1_damage = int(skill1_damage_entry.get())
                skill1_cost = int(skill1_cost_var.get())
                skill1=(skill1_damage, skill1_cost)
                print(skill1)
                skill2_damage = int(skill2_damage_entry.get())
                skill2_cost = int(skill2_cost_var.get())
                skill2=(skill2_damage, skill2_cost)
                special_skill1 = special_skill1_var.get()
                special_skill2 = special_skill2_var.get()
                skill1type = random.choices([0, 1], weights=[0.95, 0.05])[0]
                skill2type = random.choices([0, 1], weights=[0.95, 0.05])[0]
                total = random.randint(9, 15)
                new_pokemon =Pokemon(name, HP, attribute, skill1, skill2, special_skill1, special_skill2, weaknesses,
                        resistances, skill1type, skill2type, total)
                write_log(f"增加宝可梦信息为： 名称：{name}，生命值：{HP}，属性：{attribute}，弱点：{weaknesses}，抵抗：{resistances}，技能1攻击值：{skill1[0]}，技能1消耗：{skill1[1]}，技能2攻击值：{skill2[0]}，技能2消耗：{skill2[1]}，特殊技能1：{special_skill1}，特殊技能1：{special_skill1}")
                self.pokemons.append(new_pokemon)  # 将新宝可梦添加到宝可梦列表
                self.all_pokemon_list = [pokemon.name for pokemon in self.pokemons]
                self.attribute_groups = self.group_pokemons_by_attribute()
                print(new_pokemon)  # 输出新增的宝可梦信息（可选）
                write(self.pokemons)
        save_button = Button(add_window, text="保存宝可梦", command=save_pokemon, bg="#4CAF50", fg="white")
        save_button.grid(row=11, column=1, pady=10)
        close_button = Button(add_window, text="关闭", command=add_window.destroy, bg="#f44336", fg="white")
        close_button.grid(row=11, column=0, pady=10)
    def modify_pokemon(self):
        print("修改宝可梦")
        write_log('打开修改宝可梦功能')
        modify_window = Toplevel(self.root)
        modify_window.title("修改宝可梦")
        result_listbox = Listbox(modify_window, height=10, width=50)
        result_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        def populate_listbox(listbox):
            """初始化宝可梦列表框，将所有宝可梦添加到列表中"""
            listbox.delete(0, 'end')  # 清空列表框
            for pokemon in self.pokemons:
                listbox.insert('end', pokemon.name)  # 将宝可梦名称添加到列表框中
        populate_listbox(result_listbox)
        Label(modify_window, text="请输入查询宝可梦名称:").grid(row=0, column=0, padx=5, pady=5)
        search_entry = Entry(modify_window, width=30)
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        pokemon_to_modify = None  # 初始化变量
        def perform_query():
            Q_name = search_entry.get()
            nonlocal pokemon_to_modify
            try:
                pokemon_to_modify = [pokemon for pokemon in self.pokemons if pokemon.name == Q_name][0]
                update_fields()
            except IndexError:
                messagebox.showwarning("宝可梦不存在", "没有找到宝可梦，请重新输入！")
        def update_suggestions(event=None):
            query = search_entry.get()  # 获取输入内容并转换为小写
            result_listbox.delete(0, tk.END)  # 清空 Listbox
            if query.strip():  # 非空查询
                best_matches = process.extract(query, self.all_pokemon_list, limit=10)  # 返回最相关的5个
                for match in best_matches:
                    result_listbox.insert(tk.END, match[0])  # 将匹配结果加入 Listbox
        def fill_entry_from_listbox(event):
            selected_index = result_listbox.curselection()
            if selected_index:
                selected_value = result_listbox.get(selected_index)
                search_entry.delete(0, tk.END)  # 清空输入框
                search_entry.insert(0, selected_value)  # 填入选中的名称
                update_suggestions(None)
                perform_query()
        query_button = Button(modify_window, text="查询", command=perform_query)
        query_button.grid(row=0, column=2, padx=5, pady=5)
        search_entry.bind('<KeyRelease>', update_suggestions)  # 键盘释放时更新候选项
        result_listbox.bind('<<ListboxSelect>>', fill_entry_from_listbox)  # 点击 Listbox 项填入输入框
        print("sadas")
        def update_fields():
            print("sadas2", pokemon_to_modify)
            if pokemon_to_modify:
                name_entry.config(state="normal")  # 设置为只读，禁止修改
                print("sadas",pokemon_to_modify)
                name_entry.delete(0, tk.END)
                name_entry.insert(0, pokemon_to_modify.name)
                HP_entry.delete(0, tk.END)
                HP_entry.insert(0, pokemon_to_modify.health)
                attribute_var.set(pokemon_to_modify.attribute)
                weaknesses_var.set(pokemon_to_modify.weaknesses[0])
                resistances_var.set(pokemon_to_modify.resistances[0])
                skill1_damage_entry.delete(0, tk.END)
                skill1_damage_entry.insert(0, pokemon_to_modify.skill1[0])
                skill1_cost_var.set(pokemon_to_modify.skill1[1])
                skill2_damage_entry.delete(0, tk.END)
                skill2_damage_entry.insert(0, pokemon_to_modify.skill2[0])
                skill2_cost_var.set(pokemon_to_modify.skill2[1])
                special_skill1_var.set(pokemon_to_modify.special_skill1)
                special_skill2_var.set(pokemon_to_modify.special_skill2)
                name_entry.config(state="readonly")  # 设置为只读，禁止修改
            else:
                messagebox.showwarning("未选择宝可梦", "请查询并选择一个宝可梦进行修改！")
        def save_modified_pokemon():
            name = name_entry.get()
            attribute = attribute_var.get()
            weaknesses = weaknesses_var.get()
            resistances = resistances_var.get()
            HP = int(HP_entry.get())
            skill1_damage = int(skill1_damage_entry.get())
            skill1_cost = int(skill1_cost_var.get())
            skill1 = (skill1_damage, skill1_cost)
            skill2_damage = int(skill2_damage_entry.get())
            skill2_cost = int(skill2_cost_var.get())
            skill2 = (skill2_damage, skill2_cost)
            special_skill1 = special_skill1_var.get()
            special_skill2 = special_skill2_var.get()
            skill1type = random.choices([0, 1], weights=[0.95, 0.05])[0]
            skill2type = random.choices([0, 1], weights=[0.95, 0.05])[0]
            total = random.randint(9, 15)
            modified_pokemon = Pokemon(
                name, HP, attribute, skill1, skill2, special_skill1, special_skill2,
                weaknesses, resistances, skill1type, skill2type, total
            )
            write_log(
                f"将 {name} 的各属性修改为：生命值：{HP}，属性：{attribute}，弱点：{weaknesses}，抵抗：{resistances}，技能1攻击值：{skill1[0]}，技能1消耗：{skill1[1]}，技能2攻击值：{skill2[0]}，技能2消耗：{skill2[1]}，特殊技能1：{special_skill1}，特殊技能1：{special_skill1}")
            for idx, p in enumerate(self.pokemons):
                if p.name == pokemon_to_modify.name:
                    self.pokemons[idx] = modified_pokemon
                    break
            self.attribute_groups = self.group_pokemons_by_attribute()
            write(self.pokemons)
            messagebox.showinfo("修改成功", f"宝可梦 {name} 信息已修改！")
        Label(modify_window, text="名称:").grid(row=2, column=0, padx=5, pady=5)
        name_entry = Entry(modify_window, width=30)
        name_entry.grid(row=2, column=1, padx=5, pady=5)
        Label(modify_window, text="HP:").grid(row=3, column=0, padx=5, pady=5)
        HP_entry = Entry(modify_window, width=30)
        HP_entry.grid(row=3, column=1, padx=5, pady=5)
        Label(modify_window, text="属性:").grid(row=4, column=0, padx=5, pady=5)
        attribute_options = ['光', '水', '火', '暗', '草', '电', '力']
        attribute_var = StringVar()
        attribute_menu = OptionMenu(modify_window, attribute_var, *attribute_options)
        attribute_menu.grid(row=4, column=1, padx=5, pady=5)
        Label(modify_window, text="弱点:").grid(row=5, column=0, padx=5, pady=5)
        weaknesses_options = ["力", "光", "暗", "火", "草", "水", "电", "无"]
        weaknesses_var = StringVar()
        weaknesses_menu = OptionMenu(modify_window, weaknesses_var, *weaknesses_options)
        weaknesses_menu.grid(row=5, column=1, padx=5, pady=5)
        Label(modify_window, text="抵抗:").grid(row=6, column=0, padx=5, pady=5)
        resistances_options = ["力", "光", "暗", "火", "草", "水", "电", "无", "全"]
        resistances_var = StringVar()
        resistances_menu = OptionMenu(modify_window, resistances_var, *resistances_options)
        resistances_menu.grid(row=6, column=1, padx=5, pady=5)
        Label(modify_window, text="技能1伤害:").grid(row=7, column=0, padx=5, pady=5)
        skill1_damage_entry = Entry(modify_window, width=30)
        skill1_damage_entry.grid(row=7, column=1, padx=5, pady=5)
        Label(modify_window, text="技能1消耗点数 (1-4):").grid(row=8, column=0, padx=5, pady=5)
        skill1_cost_var = StringVar()
        skill1_cost_menu = OptionMenu(modify_window, skill1_cost_var, *['1', '2', '3', '4'])
        skill1_cost_menu.grid(row=8, column=1, padx=5, pady=5)
        Label(modify_window, text="技能2伤害:").grid(row=9, column=0, padx=5, pady=5)
        skill2_damage_entry = Entry(modify_window, width=30)
        skill2_damage_entry.grid(row=9, column=1, padx=5, pady=5)
        Label(modify_window, text="技能2消耗 (1-4):").grid(row=10, column=0, padx=5, pady=5)
        skill2_cost_var = StringVar()
        skill2_cost_menu = OptionMenu(modify_window, skill2_cost_var, *['1', '2', '3', '4'])
        skill2_cost_menu.grid(row=10, column=1, padx=5, pady=5)
        Label(modify_window, text="特殊技能1:").grid(row=11, column=0, padx=5, pady=5)
        special_skill1_var = StringVar()
        special_skill1_menu = OptionMenu(modify_window, special_skill1_var,
                                         *["无", "盾牌", "反射伤害", "急速攻击", "治疗", "燃烧", "克制"])
        special_skill1_menu.grid(row=11, column=1, padx=5, pady=5)
        Label(modify_window, text="特殊技能2:").grid(row=12, column=0, padx=5, pady=5)
        special_skill2_var = StringVar()
        special_skill2_menu = OptionMenu(modify_window, special_skill2_var,
                                         *["无", "盾牌", "反射伤害", "急速攻击", "治疗", "燃烧", "克制"])
        special_skill2_menu.grid(row=12, column=1, padx=5, pady=5)
        save_button = Button(modify_window, text="保存修改", command=save_modified_pokemon, bg="#4CAF50", fg="white")
        save_button.grid(row=13, column=1, pady=10)
        close_button = Button(modify_window, text="关闭", command=modify_window.destroy, bg="#f44336", fg="white")
        close_button.grid(row=14, column=0, pady=10)
    def delete_pokemon(self):
        print("删除宝可梦")
        write_log('打开删除宝可梦功能')
        delete_window = tk.Toplevel(self.root)
        delete_window.title("删除宝可梦")
        result_listbox = Listbox(delete_window, height=10, width=50)
        result_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        def populate_listbox(listbox):
            """初始化宝可梦列表框，将所有宝可梦添加到列表中"""
            listbox.delete(0, 'end')  # 清空列表框
            for pokemon in self.pokemons:
                listbox.insert('end', pokemon.name)  # 将宝可梦名称添加到列表框中
        populate_listbox(result_listbox)
        details_label = Label(delete_window, text="宝可梦详细信息将显示在这里", justify="left")
        details_label.grid(row=2, column=0, columnspan=3, padx=5, pady=10)
        def show_details(selected_pokemon):
            """展示选中的宝可梦的详细信息"""
            details = ""
            s1 = f"名称: {selected_pokemon.name}  属性： {selected_pokemon.attribute}  HP： {selected_pokemon.health}  弱点： {selected_pokemon.weaknesses[0]}  抵抗： {selected_pokemon.resistances[0]}\n"
            s2 = f"技能1伤害：{selected_pokemon.skill1[0]}  技能1消耗：{selected_pokemon.skill1[1]}  技能2伤害：{selected_pokemon.skill2[0]} 技能2消耗：{selected_pokemon.skill2[1]}\n"
            s3 = f"特殊技能1：{selected_pokemon.special_skill1}  特殊技能2：{selected_pokemon.special_skill2} \n"
            details += s1
            details += s2
            details += s3
            details_label.config(text=details)
        def perform_delete():
            """删除选中的宝可梦"""
            selected_name = search_entry.get()
            try:
                selected_pokemon = [pokemon for pokemon in self.pokemons if pokemon.name == selected_name][0]
                confirm = messagebox.askyesno("确认删除", f"您确定要删除宝可梦 {selected_pokemon.name} 吗？")
                if confirm:
                    self.pokemons = [pokemon for pokemon in self.pokemons if pokemon.name != selected_name]
                    self.all_pokemon_list = [pokemon.name for pokemon in self.pokemons]
                    self.attribute_groups = self.group_pokemons_by_attribute()
                    write(self.pokemons)
                    populate_listbox(result_listbox)  # 更新列表
                    details_label.config(text="")  # 清空详细信息
                    messagebox.showinfo("删除成功", f"宝可梦 {selected_pokemon.name} 已成功删除！")
                    write_log(f"宝可梦 {selected_pokemon.name} 已成功删除！")
                    self.attribute_groups = self.group_pokemons_by_attribute()
                else:
                    details_label.config(text="宝可梦未被删除。")
            except IndexError:
                messagebox.showwarning("宝可梦不存在", "请选择一个宝可梦进行删除！")
        def update_suggestions(event=None):
            """根据输入动态更新候选项列表框"""
            query = search_entry.get()  # 获取输入内容并转换为小写
            result_listbox.delete(0, 'end')  # 清空 Listbox
            if query.strip():  # 非空查询
                best_matches = process.extract(query, self.all_pokemon_list, limit=10)  # 返回最相关的5个
                for match in best_matches:
                    result_listbox.insert(tk.END,
                                          match[0] + "    (相似度): " + str(match[1]) + "%")  # 将匹配结果加入 Listbox
        Label(delete_window, text="请输入宝可梦名称:").grid(row=0, column=0, padx=5, pady=5)
        search_entry = Entry(delete_window, width=30)
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        query_button = Button(delete_window, text="删除", command=perform_delete)
        query_button.grid(row=3, column=2, padx=5, pady=5)
        def fill_entry_from_listbox(event):
            selected_index = result_listbox.curselection()
            if selected_index:
                selected_value = result_listbox.get(selected_index)
                pokemon_name = selected_value.split("    (相似度): ")[0]  # 提取 "相似度" 前面的名称部分
                search_entry.delete(0, 'end')  # 清空输入框
                search_entry.insert(0, pokemon_name)  # 填入选中的名称
                selected_pokemon = [pokemon for pokemon in self.pokemons if pokemon.name == pokemon_name][0]
                show_details(selected_pokemon)
        search_entry.bind('<KeyRelease>', update_suggestions)  # 键盘释放时更新候选项
        result_listbox.bind('<<ListboxSelect>>', fill_entry_from_listbox)  # 点击 Listbox 项填入输入框
        Button(delete_window, text="关闭", command=delete_window.destroy).grid(row=3, column=1, pady=10)
    def version_control(self):
        write_log("打开版本控制功能")
        self.bai_frame.pack_forget()  # 隐藏主界面
        self.version_control_window = tk.Frame(self.root)
        title_label = tk.Label(self.version_control_window, text="版本控制", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)  # 添加到顶部，并设置上方间距
        self.version_control_window.pack(pady=20)
        def store_version():
            """存储当前版本"""
            def get_backup_description():
                backup_description = description_entry.get()
                if not backup_description.strip():
                    backup_description = "备份"  # 默认内容
                return backup_description
            input_window = tk.Toplevel(self.root)
            input_window.title("请输入备份说明")
            description_label = tk.Label(input_window, text="请输入版本说明：", font=("Arial", 12))
            description_label.pack(padx=20, pady=10)
            description_entry = tk.Entry(input_window, font=("Arial", 12))
            description_entry.insert(0, "备份")  # 设置默认内容为 "备份"
            description_entry.pack(padx=20, pady=10)
            def on_confirm():
                backup_description = get_backup_description()
                input_window.destroy()  # 关闭输入框窗口
                save_version_with_description(backup_description)
            confirm_button = tk.Button(input_window, text="确定", command=on_confirm, font=("Arial", 12), bg="#32CD32")
            confirm_button.pack(pady=10)
            cancel_button = tk.Button(input_window, text="取消", command=input_window.destroy, font=("Arial", 12),
                                      bg="#A9A9A9")
            cancel_button.pack(pady=10)
        def save_version_with_description(description):
            version_folders = [folder for folder in os.listdir(self.pokemon_directory) if folder.startswith("V")]
            version_folders.sort()  # 按照文件夹名称排序
            next_version = f"V{len(version_folders) + 1}"
            version_folder = os.path.join(self.pokemon_directory, next_version)
            os.makedirs(version_folder)
            current_pokemon_file = "PokeMon.py"
            current_pokemon_txt = "pokemons.txt"
            readme_file = "readme.txt"
            rank_pokemon_txt = "rank.txt"
            if not os.path.exists(current_pokemon_file) or not os.path.exists(current_pokemon_txt):
                messagebox.showwarning("文件缺失", "当前目录下的文件 PokeMon.py 或 pokemon.txt 不存在！")
                return
            if not os.path.exists(rank_pokemon_txt):
                messagebox.showwarning("文件缺失", "当前目录下的文件 rank.txt 不存在！")
                return
            with open(os.path.join(version_folder, readme_file), "w", encoding="utf-8") as readme:
                readme.write(description)
            with open(readme_file, "w", encoding="utf-8") as readme:
                readme.write(description)
            shutil.copy(current_pokemon_file, os.path.join(version_folder, current_pokemon_file))
            shutil.copy(current_pokemon_txt, os.path.join(version_folder, current_pokemon_txt))
            shutil.copy( rank_pokemon_txt , os.path.join(version_folder,  rank_pokemon_txt ))
            write_log(f"版本 {next_version} 已成功存储！")
            messagebox.showinfo("版本存储成功", f"版本 {next_version} 已成功存储！")
        def restore_version():
            """恢复版本"""
            version_folders = [folder for folder in os.listdir(self.pokemon_directory) if folder.startswith("V")]
            if not version_folders:
                messagebox.showwarning("没有版本", "没有可用的版本进行恢复！")
                return
            version_folders.sort()  # 按照版本号排序
            restore_window = tk.Toplevel(self.root)
            restore_window.title("选择恢复版本")
            version_listbox = tk.Listbox(restore_window, height=10, width=50)
            for folder in version_folders:
                version_listbox.insert(tk.END, folder)
            version_listbox.grid(row=0, column=0, padx=20, pady=10)
            def on_version_select(event):
                selected_version_index = version_listbox.curselection()
                if selected_version_index:
                    selected_version = version_folders[selected_version_index[0]]
                    select_files_to_restore(selected_version)
                    write_log(f"选择 {selected_version} 进行恢复")
            version_listbox.bind('<<ListboxSelect>>', on_version_select)
            close_button = tk.Button(restore_window, text="关闭", command=restore_window.destroy, font=("Arial", 12),
                                     bg="#A9A9A9")
            close_button.grid(row=1, column=0, padx=20, pady=10)
        def select_files_to_restore(selected_version):
            """选择要恢复的文件"""
            file_select_window = tk.Toplevel(self.root)
            file_select_window.title(f"选择恢复文件 - {selected_version}")
            file_choices = ["PokeMon.py", "pokemons.txt", "readme.txt", "rank.txt"]
            file_listbox = tk.Listbox(file_select_window, height=4, selectmode=tk.MULTIPLE, width=50)
            for file in file_choices:
                file_listbox.insert(tk.END, file)
            file_listbox.grid(row=0, column=0, padx=20, pady=10)
            def restore_files():
                selected_files = file_listbox.curselection()
                if not selected_files:
                    messagebox.showwarning("未选择文件", "请选择要恢复的文件！")
                    return
                version_folder_path = os.path.join(self.pokemon_directory, selected_version)
                tt=""
                for file_index in selected_files:
                    file_to_restore = file_choices[file_index]
                    file_path = os.path.join(version_folder_path, file_to_restore)
                    if os.path.exists(file_path):
                        shutil.copy(file_path, file_to_restore)
                        messagebox.showinfo("版本恢复成功", f"{file_to_restore} 已成功恢复！")
                        tt+=f"版本{ selected_version} 的  {file_to_restore} 已成功恢复！"
                    else:
                        messagebox.showwarning("文件丢失", f"版本 {selected_version} 中的 {file_to_restore} 文件丢失！")
                        tt += f"版本{selected_version} 的  {file_to_restore} 文件丢失！"
                write_log(tt)
                file_select_window.destroy()
            restore_button = tk.Button(file_select_window, text="恢复选中文件", command=restore_files,
                                       font=("Arial", 12), bg="#32CD32")
            restore_button.grid(row=1, column=0, padx=20, pady=10)
            close_button = tk.Button(file_select_window, text="关闭", command=file_select_window.destroy,
                                     font=("Arial", 12), bg="#A9A9A9")
            close_button.grid(row=2, column=0, padx=20, pady=10)
        version_store_button = tk.Button(self.version_control_window, text="存储当前版本", command=store_version,
                                             font=("Arial", 12), bg="#32CD32")
        version_store_button.pack(pady=10)
        version_restore_button = tk.Button(self.version_control_window, text="恢复版本", command=restore_version,
                                               font=("Arial", 12), bg="#FF6347")
        version_restore_button.pack(pady=10)
        version_destory_button = tk.Button(self.version_control_window, text="关闭", command=self.return_to_mainn1,
                                           font=("Arial", 12), bg="#FE3547")
        version_destory_button.pack(pady=10)
    def view_log(self):
        print("日志功能")
        self.bai_frame.pack_forget()
        self.log_frame = tk.Frame(self.root)
        self.log_frame.pack(padx=20, pady=20)
        self.log_button = tk.Button(self.log_frame, text="查看日志", command=self.v_log, font=("Arial", 12))
        self.log_button.pack(pady=10)
        self.some_button = tk.Button(self.log_frame, text="测试日志功能", command=self.some_operation,
                                     font=("Arial", 12))
        self.some_button.pack(pady=10)
        self.clear_log_button = tk.Button(self.log_frame, text="清空日志", command=self.clear_log, font=("Arial", 12),
                                          bg="#FF6347")
        self.clear_log_button.pack(pady=10)
        self.b_button = tk.Button(self.log_frame, text="关闭", command=self.return_to_mainn2,
                                     font=("Arial", 12))
        self.b_button.pack(pady=10)
    def clear_log(self):
        """清空日志文件"""
        try:
            with open(self.log_txt, 'w') as f:
                write_log('日志已清空')
            messagebox.showinfo("清空日志", "日志已成功清空！")
        except Exception as e:
            messagebox.showerror("清空失败", f"无法清空日志文件: {str(e)}")
            print(f"清空日志时发生错误: {e}")
    def some_operation(self):
        """执行某个操作并记录日志"""
        write_log("执行了测试日志功能，查看日志1功能是否正常")
        print("测试日志功能操作执行中...")
    def v_log(self):
        write_log("查看了日志内容")
        """查看日志内容"""
        with open("log.txt", "r") as file:
            log_content = file.read()
        log_window = tk.Toplevel(self.root)
        log_window.title("日志内容")
        log_text = tk.Text(log_window, width=80, height=20)
        log_text.insert(tk.END, log_content)
        log_text.pack(padx=20, pady=20)
    def update_suggestions(self, event):
        """实时更新输入框下方的备选项"""
        query = self.entry.get()
        self.suggestion_box.delete(0, tk.END)  # 清空旧的建议列表
        if query.strip():  # 非空查询
            best_matches = process.extract(query, self.all_pokemon_list, limit=10)  # 返回最相关的5个
            for match in best_matches:
                self.suggestion_box.insert(tk.END, match[0]+"    (相似度): "+str(match[1])+"%")  # 将匹配结果加入 Listbox
    def update_suggestions1(self, event):
        """实时更新输入框下方的备选项"""
        query = self.team_name_entry.get()
        print(query)
        self.suggestion_box1.delete(0, tk.END)  # 清空旧的建议列表
        teamname = []
        teamsize=int(self.team_size_var.get())
        if(teamsize==2):
            for name, score in self.rank_system.team2_rankings.items():
                print(name)
                teamname.append(name)
        if teamsize==3:
            for name, score in self.rank_system.team3_rankings.items():
                teamname.append(name)
        if teamsize==5:
            for name, score in self.rank_system.team5_rankings.items():
                teamname.append(name)
        if teamsize== 7:
            for name, score in self.rank_system.team7_rankings.items():
                teamname.append(name)
        print(teamname)
        if query.strip():  # 非空查询
            best_matches = process.extract(query, teamname, limit=10)  # 返回最相关的5个
            for match in best_matches:
                self.suggestion_box1.insert(tk.END, match[0]+"    (相似度): "+str(match[1])+"%")  # 将匹配结果加入 Listbox
    def fill_entry_from_listbox(self, event):
        """当用户点击下拉列表中的项目时，将其填入输入框"""
        self.shuru=1
        selected_index = self.suggestion_box.curselection()
        if selected_index:
            selected_value = self.suggestion_box.get(selected_index)
            pokemon_name = selected_value.split("    (相似度): ")[0]  # 提取 "相似度" 前面的名称部分
            self.name=pokemon_name
            print(pokemon_name)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, pokemon_name)
            self.update_suggestions(None)
    def fill_entry_from_listbox1(self, event):
        """当用户点击下拉列表中的项目时，将其填入输入框"""
        selected_index = self.suggestion_box1.curselection()
        if selected_index:
            selected_value = self.suggestion_box1.get(selected_index)
            print(selected_value)
            pokemon_name = selected_value.split("    (相似度): ")[0]  # 提取 "相似度" 前面的名称部分
            self.name = pokemon_name
            print(pokemon_name)
            self.team_name_entry.delete(0, tk.END)
            self.team_name_entry.insert(0, pokemon_name)
            self.update_suggestions1(None)
    def search(self):
        query = self.entry.get()
        best_matches = process.extract(query, self.all_pokemon_list, limit=10)
        self.result_text.delete('1.0', tk.END)
        for match in best_matches:
            self.result_text.insert(tk.END, f"{match[0]} (相似度: {match[1]}%)\n")
    def training(self):
        self.main_frame.pack_forget()  # 隐藏主界面
        self.whehter = "正常天气"
        write_log("打开历练模式界面")
        self.training_frame = tk.Frame(self.root)
        self.training_frame.pack(pady=20)
        self.fanhui_button = tk.Button(self.training_frame, text="返回",
                                                     command=self.return_to_main5,
                                                     font=("Arial", 14))
        self.fanhui_button.pack(pady=10)
        self.team_training_battle_button = tk.Button(self.training_frame, text="团队历练模式", command=self.open_training_battle,
                                                font=("Arial", 14))
        self.team_training_battle_button.pack(pady=10)
        self.sigle_training_battle_button = tk.Button(self.training_frame, text="个人历练模式",
                                                     command=self.sig_training_battle,
                                                     font=("Arial", 14))
        self.sigle_training_battle_button.pack(pady=10)
    def sig_training_battle(self):
        """打开历练模式界面"""
        write_log("打开个人历练模式界面")
        self.training_frame.pack_forget()  # 隐藏主界面
        self.sig_training_battle_frame = tk.Frame(self.root)
        self.sig_training_battle_frame.pack(pady=20)
        self.back_buttonq = tk.Button(self.sig_training_battle_frame, text="返回", command=self.return_to_main4,
                                     font=("Arial", 14))
        self.back_buttonq.grid(row=0, column=0, padx=10, pady=15, sticky="w")
        self.mode_var = tk.StringVar(value="正常战斗模式")  # 默认选中 normal mode
        self.normal_button = tk.Radiobutton(self.sig_training_battle_frame, text="正常战斗模式", variable=self.mode_var,
                                            value="正常战斗模式",
                                            command=self.on_mode_change)
        self.clone_button = tk.Radiobutton(self.sig_training_battle_frame, text="克隆模式", variable=self.mode_var,
                                           value="克隆模式",
                                           command=self.on_mode_change)
        self.normal_button.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        self.clone_button.grid(row=0, column=2, padx=10, pady=15, sticky="w")
        self.mode_var1 = tk.StringVar(value="不写")  # 默认选中 normal mode
        self.normal_button1 = tk.Radiobutton(self.sig_training_battle_frame, text="结果写入文件", variable=self.mode_var1,
                                            value="写",
                                            command=self.on_mode_change1)
        self.clone_button1 = tk.Radiobutton(self.sig_training_battle_frame, text="结果不写入文件", variable=self.mode_var1,
                                           value="不写",
                                           command=self.on_mode_change1)
        self.normal_button1.grid(row=0, column=3, padx=10, pady=15, sticky="w")
        self.clone_button1.grid(row=0, column=4, padx=10, pady=15, sticky="w")
        self.attribute_labelq1 = tk.Label(self.sig_training_battle_frame, text="选择进行历练宝可梦的属性", font=("Arial", 14))
        self.attribute_labelq1.grid(row=1, column=0, padx=10)
        self.attribute_listboxq_1 = tk.Listbox(self.sig_training_battle_frame, height=6, width=20, selectmode=tk.SINGLE)
        self.attribute_listboxq_1.grid(row=2, column=0, padx=10)
        training_attributes = ['力', '电', '水', '火', '光', '暗', '草', '精英', '力系精英', '电系精英', '水系精英',
                               '火系精英', '光系精英', '暗系精英', '草系精英']  # 添加精英选项
        for attribute in training_attributes:
            self.attribute_listboxq_1.insert(tk.END, attribute)
        self.attribute_listboxq_1.bind("<<ListboxSelect>>", self.update_pokemon_list3)
        self.pokemon_listboxq_1 = tk.Listbox(self.sig_training_battle_frame, height=10, width=30, selectmode=tk.SINGLE)
        self.pokemon_listboxq_1.grid(row=3, column=0, padx=10)
        self.battle_buttonq1 = tk.Button(self.sig_training_battle_frame, text="历练宝可梦确认", command=self.start_battle3,
                                        font=("Arial", 14))
        self.battle_buttonq1.grid(row=4, column=0, padx=10)
        self.start_training_battle_button = tk.Button(self.sig_training_battle_frame, text="开始历练",
                                                      command=self.sig_tr_battle, font=("Arial", 14))
        self.start_training_battle_button.grid(row=5, column=0, padx=10)
    def open_training_battle(self):
        """打开历练模式界面"""
        self.training_frame.pack_forget()  # 隐藏主界面
        write_log("打开团队历练模式界面")
        self.training_battle_frame = tk.Frame(self.root)
        self.training_battle_frame.pack(pady=20)
        self.back_button = tk.Button(self.training_battle_frame, text="返回", command=self.return_to_main3,
                                     font=("Arial", 14))
        self.back_button.grid(row=0, column=0, padx=10, pady=15, sticky="nsew")
        self.mode_var = tk.StringVar(value="正常战斗模式")  # 默认选中 normal mode
        self.normal_button = tk.Radiobutton(self.training_battle_frame, text="正常战斗模式", variable=self.mode_var,
                                            value="正常战斗模式",
                                            command=self.on_mode_change)
        self.clone_button = tk.Radiobutton(self.training_battle_frame, text="克隆模式", variable=self.mode_var,
                                           value="克隆模式",
                                           command=self.on_mode_change)
        self.normal_button.grid(row=0, column=1, padx=10, pady=15, sticky="nsew")
        self.clone_button.grid(row=0, column=2, padx=10, pady=15, sticky="nsew")
        self.mode_var1 = tk.StringVar(value="不写")  # 默认选中 normal mode
        self.normal_button1 = tk.Radiobutton(self.training_battle_frame, text="结果写入文件",
                                             variable=self.mode_var1,
                                             value="写",
                                             command=self.on_mode_change1)
        self.clone_button1 = tk.Radiobutton(self.training_battle_frame, text="结果不写入文件",
                                            variable=self.mode_var1,
                                            value="不写",
                                            command=self.on_mode_change1)
        self.normal_button1.grid(row=0, column=3, padx=10, pady=15, sticky="nsew")
        self.clone_button1.grid(row=0, column=4, padx=10, pady=15, sticky="nsew")
        self.attribute_label_training = tk.Label(self.training_battle_frame, text="选择属性进行历练",
                                                 font=("Arial", 14))
        self.attribute_label_training.grid(row=1, column=0)
        self.attribute_listbox_training = tk.Listbox(self.training_battle_frame, height=6, width=20,
                                                     selectmode=tk.SINGLE)
        self.attribute_listbox_training.grid(row=2, column=0)
        training_attributes = ['力', '电', '水', '火', '光', '暗', '草', '精英','力系精英', '电系精英', '水系精英', '火系精英', '光系精英', '暗系精英', '草系精英']  # 添加精英选项
        for attribute in training_attributes:
            self.attribute_listbox_training.insert(tk.END, attribute)
        self.result_label = tk.Label(self.training_battle_frame, text="历练结果：", font=("Arial", 14))
        self.result_label.grid(row=1, column=1, padx=10, pady=15, sticky="w")
        self.result_text = tk.Text(self.training_battle_frame, height=8, width=55, wrap=tk.WORD)
        self.result_text.grid(row=2, column=1, padx=10, pady=15)
        self.result_text.config(state=tk.DISABLED)
        self.start_training_battle_button = tk.Button(self.training_battle_frame, text="开始历练",
                                                      command=self.start_training_battle, font=("Arial", 14))
        self.start_training_battle_button.grid(row=3, column=0)
    def start_training_battle(self):
        self.attribute_groups = self.group_pokemons_by_attribute()
        """开始历练模式对战"""
        try:
            selected_attribute = self.attribute_listbox_training.get(tk.ACTIVE)
            if selected_attribute is None:
                messagebox.showwarning("选择错误", "请从属性列表中选择一个属性！")
                return
            shuxing=None
            if selected_attribute == '全体':
                shuxing = '全体'
                eligible_pokemons = self.pokemons
            elif selected_attribute == '精英':
                shuxing = '精英'
                eligible_pokemons = load_pokemons_from_file(file_path='全体jingying.txt')
            elif selected_attribute.endswith("系精英"):
                shuxing=selected_attribute[:-3]
                eligible_pokemons = load_pokemons_from_file(file_path=shuxing+'jingying'+'.txt')
            else:
                shuxing = selected_attribute
                eligible_pokemons = self.attribute_groups[selected_attribute]
            write_log(f"选择: {shuxing}  成员进行历练")
            self.training_battle(eligible_pokemons,shuxing)
        except IndexError:
            messagebox.showwarning("选择错误", "请从属性列表中选择一个属性！")
    def sig_tr_battle(self):
        selected_pokemon=[self.lilian_pokemon]
        """处理历练模式中的每一关"""
        total_battles = 30  # 总共有30关
        zhenshouPKM=[]
        for i in range(1, total_battles + 1):
            enemy_pokemon = self.create_enemy_pokemon(self.lilian_pokemon_shuxing, i)  # 根据关卡生成敌人
            print(enemy_pokemon)
            zhenshouPKM.append(enemy_pokemon)
        addtemp=[]
        for pkm in selected_pokemon:
            a=0#生命
            b=0#攻击
            for i in range(1, total_battles + 1):
                enemy_pokemon = zhenshouPKM[i-1]
                pokemon1=pkm
                pokemon2= enemy_pokemon
                pokemon1_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                     pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                     pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type,
                                     pokemon1.skill2type, pokemon1.total_points)
                pokemon2_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1,
                                     pokemon2.skill2, pokemon2.special_skill1, pokemon2.special_skill2,
                                     pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type,
                                     pokemon2.skill2type, pokemon2.total_points)
                battle_result,b_result2,result_3 = battle( pokemon1_1, pokemon2_2,"正常战斗模式",self.whehter)  # 假设有battle方法来处理战斗
                print(battle_result)
                if battle_result == f'{pkm.name}'+" 胜利":
                    if i % 2 == 1:  # 奇数
                        a += 1  # 增加生命值
                    else:  # 偶数关
                        b += 1  # 增加攻击力
                    if(i==total_battles):
                        l_temp = [a, b]
                        addtemp.append(l_temp)
                else:
                    l_temp=[a,b]
                    addtemp.append(l_temp)
                    break
            for p in self.pokemons:
                if (p.name == pkm.name):
                    p.health+=a
                    p.skill1=(p.skill1[0]+b,p.skill1[1])
                    p.skill2=(p.skill2[0]+b,p.skill2[1])
        if(self.moshi1 == "写"):
            self.attribute_groups = self.group_pokemons_by_attribute()
            print("写入文件")
            with open("pokemons.txt", "w", encoding="utf-8") as f:
                for pkm in self.pokemons:
                    f.write(
                        f"{pkm.name},{pkm.health},{pkm.attribute},{pkm.skill1[0]},{pkm.skill1[1]},{pkm.skill2[0]},{pkm.skill2[1]},{pkm.special_skill1},{pkm.special_skill2},{','.join(pkm.weaknesses)},{','.join(pkm.resistances)},{pkm.skill1type},{pkm.skill2type},{pkm.total_points}\n")
        for i in range(len(selected_pokemon)):
            print(selected_pokemon[i].name,addtemp[i])
        write_log( f"{self.lilian_pokemon.name}  通过历练{sum(addtemp[0])}关，生命值提升{addtemp[0][0]}点， 攻击值提升{addtemp[0][1]}点")
        messagebox.showinfo("历练结果", f"{self.lilian_pokemon.name}  通过历练{sum(addtemp[0])}关，生命值提升{addtemp[0][0]}点，攻击值提升{addtemp[0][1]}点")
    def training_battle(self, selected_pokemon, selected_attribute):
        """处理历练模式中的每一关"""
        total_battles = 30  # 总共有30关
        zhenshouPKM=[]
        for i in range(1, total_battles + 1):
            enemy_pokemon = self.create_enemy_pokemon(selected_attribute, i)  # 根据关卡生成敌人
            print(enemy_pokemon)
            zhenshouPKM.append(enemy_pokemon)
        addtemp=[]
        for pkm in selected_pokemon:
            a=0#生命
            b=0#攻击
            for i in range(1, total_battles + 1):
                enemy_pokemon = zhenshouPKM[i-1]
                pokemon1=pkm
                pokemon2= enemy_pokemon
                pokemon1_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                     pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                     pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type,
                                     pokemon1.skill2type, pokemon1.total_points)
                pokemon2_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1,
                                     pokemon2.skill2, pokemon2.special_skill1, pokemon2.special_skill2,
                                     pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type,
                                     pokemon2.skill2type, pokemon2.total_points)
                battle_result,b_result2,result_3 = battle( pokemon1_1, pokemon2_2,"正常战斗模式",self.whehter)  # 假设有battle方法来处理战斗
                print(battle_result)
                if battle_result == f'{pkm.name}'+" 胜利":
                    if i % 2 == 1:  # 奇数
                        a += 1  # 增加生命值
                    else:  # 偶数关
                        b += 1  # 增加攻击力
                    if(i==total_battles):
                        l_temp = [a, b]
                        addtemp.append(l_temp)
                else:
                    l_temp=[a,b]
                    addtemp.append(l_temp)
                    break
            for p in self.pokemons:
                if (p.name == pkm.name):
                    p.health+=a
                    p.skill1=(p.skill1[0]+b,p.skill1[1])
                    p.skill2=(p.skill2[0]+b,p.skill2[1])
        if (self.moshi1 == "写"):
            self.attribute_groups = self.group_pokemons_by_attribute()
            print("写入文件")
            with open("pokemons.txt", "w", encoding="utf-8") as f:
                for pkm in self.pokemons:
                    f.write(
                        f"{pkm.name},{pkm.health},{pkm.attribute},{pkm.skill1[0]},{pkm.skill1[1]},{pkm.skill2[0]},{pkm.skill2[1]},{pkm.special_skill1},{pkm.special_skill2},{','.join(pkm.weaknesses)},{','.join(pkm.resistances)},{pkm.skill1type},{pkm.skill2type},{pkm.total_points}\n")
        text="团队历练结果如下： \n"
        for i in range(len(selected_pokemon)):
            text+= f"{selected_pokemon[i].name}  增加血量： {addtemp[i][0]}   增加攻击值： {addtemp[i][1]}\n"
            print(selected_pokemon[i].name,addtemp[i])
        write_log(text)
        self.result_text.config(state=tk.NORMAL)  # 允许编辑
        self.result_text.delete(1.0, tk.END)  # 清空现有内容
        self.result_text.insert(tk.END, text)  # 显示新的历练结果
        self.result_text.config(state=tk.DISABLED)  # 禁用编辑
        messagebox.showinfo("历练结束", "历练模式已结束，查看结果！")
    def create_enemy_pokemon(self, attribute, level):
        shuxing=None
        if(attribute=='精英'):
            attribute0 = ["力", "光", "暗", "火", "草", "水", "电" ]
            shuxing= random.choice(attribute0)
        else:shuxing=attribute
        """根据属性和关卡生成敌人的宝可梦"""
        name = f"{shuxing}宝可梦镇守{level}"  # 给每个敌人起个名字
        health = 100+level * 10  # 假设关卡越高敌人生命越强
        attack2 = 30+level * 7  # 攻击力随着关卡增加
        attack1 = 30 + (level-1) * 7  # 攻击力随着关卡增加
        skill1 = (random.randint(attack1, attack2), random.randint(1, 3))  # (攻击值, 消耗点数)
        skill2 = (random.randint(attack1, attack2), random.randint(1, 3))  # (攻击值, 消耗点数)
        skill1type = random.choices([0, 1], weights=[0.95, 0.05])[0]
        skill2type = random.choices([0, 1], weights=[0.95, 0.05])[0]
        special_skill1 = random.choice(special_skills)
        special_skill2 = random.choice([skill for skill in special_skills if skill != special_skill1]) if len(
            special_skills) > 1 else "无"
        attribute0 = ["力", "光", "暗", "火", "草", "水", "电", "无"]
        attribute1 = ["力", "光", "暗", "火", "草", "水", "电", "无", "全"]
        weights = [1, 1, 1, 1, 1, 1, 1, 3]  # '无' 的权重是 5，其他属性的权重是 1
        weights1 = [1, 1, 1, 1, 1, 1, 1, 3,3]  # '无' '全'的权重是 5，其他属性的权重是 1
        weaknesses =  random.choices([attr for attr in attribute0 if attr != shuxing],
                         weights=[w for i, w in enumerate(weights) if attribute0[i] != shuxing],
                         k=1)
        resistances =  random.choices([attr for attr in attribute1 if attr != shuxing],
                         weights=[w for i, w in enumerate(weights1) if attribute1[i] != shuxing],
                         k=1)
        total = random.randint(9, 15)
        return Pokemon(name, health, attribute, skill1, skill2, special_skill1, special_skill2, weaknesses, resistances,
                       skill1type, skill2type, total)
    def on_mode_change(self):
        selected_mode = self.mode_var.get()
        if selected_mode == "正常战斗模式":
            write_log('战斗模式选择正常战斗模式')
            self.moshi= "正常战斗模式"
            print("选择了正常战斗模式")
        elif selected_mode == "克隆模式":
            write_log('战斗模式选择克隆模式')
            print("选择了克隆模式")
            self.moshi = "克隆模式"
    def on_mode_change1(self):
        selected_mode = self.mode_var1.get()
        if selected_mode == "写":
            write_log("结果将写入文件")
            self.moshi1= "写"
            print("结果写入文件")
        elif selected_mode == "不写":
            write_log("结果不会写入文件")
            print("结果不写入文件")
            self.moshi1 = "不写"
    def open_elimination_battle(self):
        """打开淘汰赛模式界面"""
        write_log("打开淘汰赛模式界面")
        self.main_frame.pack_forget()  # 隐藏主界面
        self.whehter = "正常天气"
        self.elimination_battle_frame = tk.Frame(self.root)
        self.elimination_battle_frame.pack(pady=20)
        self.weather_var = tk.StringVar(value="正常天气")  # 默认天气为晴天
        self.weather_menu = tk.OptionMenu(
            self.elimination_battle_frame,
            self.weather_var,  # 绑定天气变量
            "正常天气", "重力太空", "极热沙漠", "暗黑界域", "海洋之星", "藤蔓之眼", "光明城堡", "雷霆风暴", "众生平等",
            command=self.on_weather_change  # 回调函数
        )
        self.weather_menu.grid(row=0, column=0, padx=10, pady=10)
        self.back_button = tk.Button(self.elimination_battle_frame, text="返回",
                                     command=self.return_to_main2, font=("Arial", 14))
        self.back_button.grid(row=0, column=3, padx=10, pady=15, sticky="w")
        self.attribute_label_elimination = tk.Label(self.elimination_battle_frame, text="选择属性进行淘汰赛",
                                                    font=("Arial", 14))
        self.attribute_label_elimination.grid(row=1, column=0, pady=10, columnspan=3)
        self.attribute_listbox_elimination = tk.Listbox(self.elimination_battle_frame, height=6, width=20,
                                                        selectmode=tk.SINGLE)
        self.attribute_listbox_elimination.grid(row=2, column=0, columnspan=3, pady=10)
        shuxinglist = list(self.attribute_groups.keys())
        shuxinglist.append('全体')
        shuxinglist.append('精英')
        print(shuxinglist)
        for attribute in shuxinglist:
            self.attribute_listbox_elimination.insert(tk.END, attribute)
        self.canvas1 = tk.Canvas(self.elimination_battle_frame)
        self.scrollbar = tk.Scrollbar(self.elimination_battle_frame, orient="vertical", command=self.canvas1.yview)
        self.hscrollbar = tk.Scrollbar(self.elimination_battle_frame, orient="horizontal", command=self.canvas1.xview)
        self.canvas1.config(yscrollcommand=self.scrollbar.set, xscrollcommand=self.hscrollbar.set)
        self.result_frame = tk.Frame(self.canvas1)
        self.canvas1.create_window((0, 0), window=self.result_frame, anchor="nw")
        self.canvas1.grid(row=3, column=0, sticky="nsew", columnspan=4)
        self.scrollbar.grid(row=3, column=4, sticky="ns", columnspan=4)
        self.hscrollbar.grid(row=4, column=0, sticky="ew", columnspan=4)
        self.canvas1.bind_all("<MouseWheel>", self.on_mouse_wheel1)
        self.mode_var = tk.StringVar(value="正常战斗模式")  # 默认选中 normal mode
        self.normal_button = tk.Radiobutton(self.elimination_battle_frame, text="正常战斗模式", variable=self.mode_var,
                                            value="正常战斗模式",
                                            command=self.on_mode_change)
        self.clone_button = tk.Radiobutton(self.elimination_battle_frame, text="克隆模式", variable=self.mode_var,
                                           value="克隆模式",
                                           command=self.on_mode_change)
        self.normal_button.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        self.clone_button.grid(row=0, column=2, padx=10, pady=15, sticky="w")
        self.result_label = tk.Label(self.result_frame, text="淘汰赛结果将在此显示...", font=("Arial", 12))
        self.result_label.grid(row=3, column=0, sticky="nsew", columnspan=4)
        self.start_elimination_button = tk.Button(self.elimination_battle_frame, text="开始淘汰赛",
                                                  command=self.start_elimination_battle, font=("Arial", 14))
        self.start_elimination_button.grid(row=1, column=3, columnspan=3, pady=20)
    def start_elimination_battle(self):
        self.attribute_groups = self.group_pokemons_by_attribute()
        """开始淘汰赛对战"""
        try:
            selected_attribute = self.attribute_listbox_elimination.get(tk.ACTIVE)
            if selected_attribute is None:
                messagebox.showwarning("选择错误", "请从属性列表中选择一个属性！")
                return
            LB=1
            if selected_attribute == '全体':
                eligible_pokemons = self.pokemons
                LB = 1
            elif selected_attribute == '精英':
                eligible_pokemons = load_pokemons_from_file(file_path='全体jingying.txt')
                LB = 2
            else:
                eligible_pokemons = self.attribute_groups[selected_attribute]
                LB = 3
            write_log(f"选择: {selected_attribute} 成员进行淘汰赛对战")
            random.shuffle(eligible_pokemons)
            self.run_tournament(eligible_pokemons,LB)
        except IndexError:
            messagebox.showwarning("选择错误", "请从属性列表中选择一个属性！")
    def display_elimination_tournament(self,pokemons, canvas,LB):
        """展示淘汰赛的树状图"""
        canvas.delete("all")  # 清空画布
        round_number = 1
        pokemons, bye_pokemons = self.handle_bye_pokemons(pokemons)
        y_offset = 20  # 设置每轮之间的垂直间距
        current_round_pokemons = pokemons
        all_rounds = []  # 用于存储每轮的对战信息
        ADDSCORE=50
        if(LB==3):
            ADDSCORE = 30
        while len(current_round_pokemons) > 1:
            num_matches = len(current_round_pokemons) // 2
            next_round_pokemons = []
            round_matches = []
            for i in range(0, len(current_round_pokemons), 2):
                if i + 1 < len(current_round_pokemons):
                    flag = True
                    winname = None
                    winner = None
                    pokemon1 = current_round_pokemons[i]
                    pokemon2 = current_round_pokemons[i + 1]
                    num=1
                    while(flag):
                        pokemon1_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                                                                      pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                                                                      pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type,
                                                                                      pokemon1.skill2type, pokemon1.total_points)
                        pokemon2_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1,
                                                                                      pokemon2.skill2, pokemon2.special_skill1, pokemon2.special_skill2,
                                                                                      pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type,
                                                                                      pokemon2.skill2type, pokemon2.total_points)
                        winner_text, winner ,result_3= battle(pokemon1_1, pokemon2_2,self.moshi,self.whehter)
                        if  winner_text == f"{pokemon1_1.name} 胜利":
                            flag = False
                            winname=pokemon1_1.name
                            pokemon1.person_score += ADDSCORE
                            self.rank_system.update_pokemon_rank(pokemon1)
                            winner=pokemon1
                        elif  winner_text ==f"{pokemon2_2.name} 胜利":
                            flag = False
                            winname = pokemon2_2.name
                            pokemon2.person_score += ADDSCORE
                            self.rank_system.update_pokemon_rank(pokemon2)
                            winner=pokemon2
                        else:
                            flag=True
                            if (num>5):
                                flag = False
                                options=[current_round_pokemons[i],current_round_pokemons[i+1]]
                                selected_option = random.choice(options)
                                winname = selected_option.name
                                selected_option.person_score += ADDSCORE
                                self.rank_system.update_pokemon_rank(selected_option)
                                winner =selected_option
                            num+=1
                    round_matches.append((pokemon1.name, pokemon2.name, winname))
                    next_round_pokemons.append(winner)
            if(round_number==1):
                for i in bye_pokemons:
                    pokemon1 = i
                    pokemon1.person_score += ADDSCORE
                    self.rank_system.update_pokemon_rank(pokemon1)
                    round_matches.append((pokemon1.name, "轮空", pokemon1.name))  # 轮空选手直接晋级
                    next_round_pokemons.append(pokemon1)
            all_rounds.append(round_matches)
            current_round_pokemons = next_round_pokemons
            round_number += 1
        winner = current_round_pokemons[0]
        winner.person_score += ADDSCORE
        self.rank_system.update_pokemon_rank( winner)
        save_rank_data(self.rank_system)
        self.rank_system.print_pokemon_rankings()
        canvas.create_text(300, y_offset, text=f"最终胜者: {winner.name}", font=("Arial", 16),fill="red")
        print("计算完成")
        self.print_tournament_tree(all_rounds)
        self.draw_matches(all_rounds, canvas, y_offset)
    def print_tournament_tree(self,all_rounds):
        print("淘汰赛赛程：")
        self.result_label.config(text="淘汰赛赛程：")  # 清空Label内容
        self.canvas1.delete("all")
        """打印淘汰赛的树状结构"""
        round_num = 1
        text_content = "淘汰赛赛程：\n"
        for round_matches in all_rounds:
            aa="    "*round_num
            print(aa)
            print(aa+f"第 {round_num} 轮:")
            bbb=aa+f"第 {round_num} 轮:"
            text_content +=bbb+"\n"
            for match in round_matches:
                pokemon1, pokemon2, winner = match
                if pokemon2 != "轮空":
                    bbbb=aa+f"  {pokemon1} vs {pokemon2} -> {winner}"
                    text_content += bbbb + "\n"
                    print(aa+f"  {pokemon1} vs {pokemon2} -> {winner}")
                else:
                    bbbb = aa+f"  {pokemon1} vs 轮空 -> {pokemon1} 晋级"
                    text_content += bbbb + "\n"
                    print(aa+f"  {pokemon1} vs 轮空 -> {pokemon1} 晋级")
            round_num += 1
        print("\n")
        write_log(text_content)
        self.result_label.config(text=text_content)
        self.canvas1.create_text(10, 10, anchor="nw", text=text_content, font=("Arial", 10))
        self.canvas1.config(scrollregion=self.canvas1.bbox("all"))
    def draw_matches(self,all_rounds, canvas, y_offset):
        x1, x2 = 100, 200
        horizontal_spacing = 280  # 水平间距，确保对战选手不重叠
        canvas_width = 10000  # 画布宽度设置为较大值，确保可以显示所有信息
        canvas.config(scrollregion=(0, 0, canvas_width, 800))  # 设置画布的可滚动区域
        aa=1
        bb=len(all_rounds)
        zb=[]
        zuobiao=[]
        for ii in range(len(all_rounds)):
            if(aa==1):
                round_matches=all_rounds[aa-1]
                num_matches = len(round_matches)
                round_y_offset = y_offset  # 每一轮的起始高度
                for i, (pokemon1, pokemon2, winner) in enumerate(round_matches):
                    match_x1 = x1 + ((i) % num_matches) * horizontal_spacing
                    match_x2 = x2 + ((i) % num_matches) * horizontal_spacing
                    canvas.create_line(match_x1, round_y_offset + aa * 30, match_x2, round_y_offset + (aa ) * 30,width=2, fill="blue")
                    canvas.create_line((match_x1 + match_x2) / 2 , round_y_offset + (aa ) * 30, (match_x1 + match_x2) / 2, round_y_offset + (aa ) * 30+40, arrow=tk.LAST,width=2, fill="green")
                    canvas.create_text(match_x1 , round_y_offset + aa * 30, text=pokemon1, anchor="e",
                                               font=("Arial", 10))
                    canvas.create_text(match_x2 , round_y_offset + (aa ) * 30, text=pokemon2, anchor="w",
                                               font=("Arial", 10))
                    if pokemon2 != "轮空":
                        temp = ((match_x1 + match_x2) / 2, round_y_offset + (aa ) * 30+50)
                        if (temp not in zuobiao):
                            zuobiao.append(temp)
                            canvas.create_text((match_x1 + match_x2) / 2, round_y_offset + (aa ) * 30+50, text=f"胜者: {winner}",
                                               font=("Arial", 10))
                    else:
                        temp = ((match_x1 + match_x2) / 2, round_y_offset + (aa) * 30 + 50)
                        if (temp not in zuobiao):
                            zuobiao.append(temp)
                            canvas.create_text((match_x1 + match_x2) / 2, round_y_offset + (aa ) * 30+50, text=f" {winner}轮空晋级",
                                               font=("Arial", 10))
            else:
                zb=zuobiao.copy()
                zuobiao.clear()
                round_matches = all_rounds[aa-1]
                for i in range(0, len(zb), 2):  # 步长为2，跳过每次的一个元素
                    t1=zb[i]
                    t2=zb[i+1]
                    zuobiao.append(((t1[0] + t2[0]) / 2,t1[1] +50 ))
                    canvas.create_line(t1[0]+50, t1[1], t2[0]-50,t2[1],width=2, fill="blue")
                    canvas.create_line((t1[0] + t2[0]) / 2, t1[1],(t1[0] + t2[0]) / 2, t2[1]+40 , arrow = tk.LAST,width=2, fill="green")
                    canvas.create_text((t1[0] + t2[0]) / 2,t1[1] +50 , text=f"胜者: {round_matches[int(i/2)][2]}",
                                       font=("Arial", 10))
                y_offset += 100  # 为下一轮的高度调整
            aa+=1
    def run_tournament(self,pokemons,LB):
        """运行比赛并展示淘汰赛树"""
        """运行比赛并展示淘汰赛树"""
        root = tk.Tk()
        root.title("淘汰赛")
        self.frame = tk.Frame(root)
        self. frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.frame, width=800, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        hbar = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.config(xscrollcommand=hbar.set)
        vbar = tk.Scrollbar( self.frame, orient="vertical", command= self.canvas.yview)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=vbar.set)
        self.display_elimination_tournament(pokemons,  self.canvas,LB)
        root.mainloop()
    def get_nearest_power_of_2(self,n):
        """计算参赛选手数量最接近的2的幂次方"""
        return 1 << (n - 1).bit_length()
    def handle_bye_pokemons(self,pokemons):
        """计算轮空的宝可梦并处理轮空"""
        n = len(pokemons)
        nearest_power_of_2 = self.get_nearest_power_of_2(n)
        bye_count = nearest_power_of_2 - n  # 需要轮空的宝可梦数量
        bye_pokemons = []
        if bye_count > 0:
            bye_pokemons = random.sample(pokemons, bye_count)  # 随机选取轮空宝可梦
            pokemons = [p for p in pokemons if p not in bye_pokemons]
        return pokemons, bye_pokemons
    def group_pokemons_by_attribute(self):
        self.all_pokemon_list = [pokemon.name for pokemon in self.pokemons]
        """根据宝可梦的属性将宝可梦分类"""
        attribute_groups = {}
        for pokemon in self.pokemons:
            if pokemon.attribute not in attribute_groups:
                attribute_groups[pokemon.attribute] = []
            attribute_groups[pokemon.attribute].append(pokemon)
        return attribute_groups
    def ranking_key(self,pokemon):
        score = pokemon.score
        head_to_head_score = sum([1 for opponent in pokemon.shuyinglist[0] if opponent in pokemon.shuyinglist[2]])
        buchholz_score = sum([opponent.score for opponent in pokemons if opponent.name in pokemon.shuyinglist[0]])
        return (-score, -head_to_head_score, -buchholz_score)  # 排名时降序排列
    def display_ranking(self,pokemon_list, K,selected_attribute):
        """显示宝可梦的排名"""
        print("循环积分赛排名：")
        self.result_label.config(text="循环积分赛排名：")  # 清空Label内容
        self.canvas.delete("all")
        # sorted_pokemons = sorted(pokemon_list, key=self.ranking_key)
        sorted_pokemons = heapq.nsmallest(K, pokemon_list, key=self.ranking_key)
        text_content = "循环积分赛排名：\n"
        attribute_scores = {}
        attribute_rank = {}
        attribute_num={}
        for rank, pokemon in enumerate(sorted_pokemons[:K], start=1):
            text_content += f"{rank}. {pokemon.name} - 积分: {pokemon.score} - 胜负关系: {pokemon.scorelist}\n"
            attribute = pokemon.attribute
            score = pokemon.score
            if attribute not in attribute_scores:
                attribute_scores[attribute] = 0  # 如果没有该属性，初始化为 0
                attribute_rank[attribute] = 0  # 如果没有该属性，初始化为 0
                attribute_num[attribute] = 0
            attribute_rank[attribute] += rank
            attribute_scores[attribute] += score  # 累加该属性的分数
            attribute_num[attribute] += 1
        txt="\n"
        for attribute, total_score in attribute_scores.items():
            print(f"属性: {attribute}进入{K}强的有{attribute_num[attribute]}个, 平均分: { round(total_score/attribute_num[attribute], 1)}, 平均排名: {round(attribute_rank[attribute]/attribute_num[attribute], 1)}")
            txt +=f"{attribute}进入{K}强的有{attribute_num[attribute]}个,均分:{ round(total_score/attribute_num[attribute], 1)},均排名: {round(attribute_rank[attribute]/attribute_num[attribute], 1)} \n"
        text_content+=txt
        write_log(text_content)
        all_pokemons=sorted_pokemons[:K]
        file_path=selected_attribute+'jingying.txt'
        with open(file_path, "w", encoding="utf-8") as f:
            for pkm in all_pokemons:
                f.write(
                    f"{pkm.name},{pkm.health},{pkm.attribute},{pkm.skill1[0]},{pkm.skill1[1]},{pkm.skill2[0]},{pkm.skill2[1]},{pkm.special_skill1},{pkm.special_skill2 },{','.join(pkm.weaknesses)},{','.join(pkm.resistances)},{int(pkm.skill1type)},{int(pkm.skill2type)},{pkm.total_points}\n")
        self.result_label.config(text=text_content)
        self.canvas.create_text(10, 10, anchor="nw", text=text_content, font=("Arial", 10))
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    def clear_placeholder(self, event):
        """输入框获得焦点时清除占位符"""
        if self.entry.get() == self.entry_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg="black")
    def clear_placeholder1(self, event):
        """输入框获得焦点时清除占位符"""
        if self.team_name_entry.get() == self.entry_placeholder1:
            self.team_name_entry.delete(0, tk.END)
            self.team_name_entry.config(fg="black")
    def restore_placeholder1(self, event):
        """输入框失去焦点时，若为空则恢复占位符"""
        if not self.team_name_entry.get():
            self.team_name_entry.insert(0, self.entry_placeholder1)
            self.team_name_entry.config(fg="grey")
    def restore_placeholder(self, event):
        """输入框失去焦点时，若为空则恢复占位符"""
        if not self.entry.get():
            self.entry.insert(0, self.entry_placeholder)
            self.entry.config(fg="grey")
    def open_single_battle(self):
        """打开单挑模式界面"""
        write_log('选择单挑模式')
        self.whehter = "正常天气"
        self.main_frame.pack_forget()  # 隐藏主界面
        self.shuru=0
        self.name=None
        self.single_battle_frame = tk.Frame(self.root)
        self.single_battle_frame.pack(pady=20)
        self.mode_var = tk.StringVar(value="正常战斗模式")  # 默认选中 normal mode
        self.normal_button = tk.Radiobutton(self.single_battle_frame, text="正常战斗模式", variable=self.mode_var,
                                            value="正常战斗模式",
                                            command=self.on_mode_change)
        self.clone_button = tk.Radiobutton(self.single_battle_frame, text="克隆模式", variable=self.mode_var, value="克隆模式",
                                           command=self.on_mode_change)
        self.normal_button.grid(row=0, column=1, padx=5, pady=10, sticky="e")
        self.clone_button.grid(row=0, column=2, padx=5, pady=10, sticky="e")
        self.back_button = tk.Button(self.single_battle_frame, text="返回", command=self.return_to_main,
                                     font=("Arial", 14))
        self.back_button.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        self.attribute_label1 = tk.Label(self.single_battle_frame, text="选择宝可梦1的属性", font=("Arial", 14))
        self.attribute_label1.grid(row=1, column=0, padx=20)
        self.attribute_listbox1 = tk.Listbox(self.single_battle_frame, height=6, width=15, selectmode=tk.SINGLE)
        self.attribute_listbox1.grid(row=2, column=0, padx=20)
        for attribute in self.attribute_groups.keys():
            self.attribute_listbox1.insert(tk.END, attribute)
        self.attribute_listbox1.bind("<<ListboxSelect>>", self.update_pokemon_list1)
        self.pokemon_listbox1 = tk.Listbox(self.single_battle_frame, height=10, width=15, selectmode=tk.SINGLE)
        self.pokemon_listbox1.grid(row=3, column=0, padx=20)
        self.pokemon_listbox1.bind("<<ListboxSelect>>", self.set_aaa_to_0)
        self.battle_button1 = tk.Button(self.single_battle_frame, text="宝可梦1确认", command=self.start_battle1, font=("Arial", 14))
        self.battle_button1.grid(row=4, column=0, pady=10)
        self.entry_placeholder = "请输入宝可梦名称..."  # 占位符文本
        self.entry = tk.Entry(self.single_battle_frame, fg="grey", font=("Arial", 12))
        self.entry.insert(0, self.entry_placeholder)
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.restore_placeholder)
        self.entry.bind('<KeyRelease>', self.update_suggestions)  # 监听输入事件
        self.entry.grid(row=1, column=1, pady=10)
        self.suggestion_box = tk.Listbox(self.single_battle_frame, height=6, width=25)  # 控制显示的备选项数量
        self.suggestion_box.grid(row=2, column=1)
        self.suggestion_box.bind('<<ListboxSelect>>', self.fill_entry_from_listbox)
        self.attribute_label2 = tk.Label(self.single_battle_frame, text="选择宝可梦2的属性", font=("Arial", 14))
        self.attribute_label2.grid(row=1, column=2, padx=20)
        self.attribute_listbox2 = tk.Listbox(self.single_battle_frame, height=6, width=15, selectmode=tk.SINGLE)
        self.attribute_listbox2.grid(row=2, column=2, padx=20)
        for attribute in self.attribute_groups.keys():
            self.attribute_listbox2.insert(tk.END, attribute)
        self.attribute_listbox2.bind("<<ListboxSelect>>", self.update_pokemon_list2)
        self.pokemon_listbox2 = tk.Listbox(self.single_battle_frame, height=10, width=15, selectmode=tk.SINGLE)
        self.pokemon_listbox2.grid(row=3, column=2, padx=20)
        self.pokemon_listbox2.bind("<<ListboxSelect>>", self.set_aaa_to_0)
        self.battle_button2 = tk.Button(self.single_battle_frame, text="宝可梦2确认", command=self.start_battle2, font=("Arial", 14))
        self.battle_button2.grid(row=4, column=2, pady=10)
        self.canvas = tk.Canvas(self.single_battle_frame)
        self.scrollbar = tk.Scrollbar(self.single_battle_frame, orient="vertical", command=self.canvas.yview)
        self.hscrollbar = tk.Scrollbar(self.single_battle_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.config(yscrollcommand=self.scrollbar.set, xscrollcommand=self.hscrollbar.set)
        self.output_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.output_frame, anchor="nw")
        self.canvas.grid(row=5, column=0, columnspan=2, pady=10,sticky="nsew")
        self.scrollbar.grid(row=5, column=2, sticky="ns")
        self.hscrollbar.grid(row=6, column=0, columnspan=2, sticky="ew")
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.label1 = tk.Label(self.output_frame, text="", font=("Arial", 10), anchor="w")
        self.label1.grid(row=5, column=0, columnspan=3, pady=10,sticky="nsew")
        self.start_battle_button = tk.Button(self.single_battle_frame, text="开始对战", command=self.start_battle, font=("Arial", 14))
        self.start_battle_button.grid(row=4, column=1, columnspan=1, pady=20)
        self.weather_var = tk.StringVar(value="正常天气")  # 默认天气为晴天
        self.weather_menu = tk.OptionMenu(
            self.single_battle_frame,
            self.weather_var,  # 绑定天气变量
            "正常天气","重力太空", "极热沙漠", "暗黑界域", "海洋之星", "藤蔓之眼", "光明城堡" , "雷霆风暴","众生平等", # 天气选项
            command=self.on_weather_change  # 回调函数
        )
        self.weather_menu.grid(row=0, column=0, padx=10, pady=10)
    def on_weather_change(self, selected_weather):
        self.whehter=selected_weather
        """当天气改变时触发"""
        write_log(f"选择天气：{selected_weather}")
        print(f"当前天气为：{selected_weather}")
    def set_aaa_to_0(self, event):
        """点击 pokemon_listbox1 设置 aaa 为 0"""
        self.shuru = 0
    def display_battle_output(self, messages):
        self.label1.config(text=messages, anchor='w', justify='left')
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    def open_tournament_battle(self):
        # print(GGG)
        """打开积分赛模式界面"""
        write_log('打开积分赛模式')
        self.whehter = "正常天气"
        self.main_frame.pack_forget()  # 隐藏主界面
        self.tournament_battle_frame = tk.Frame(self.root)
        self.tournament_battle_frame.pack(pady=20)
        self.mode_var = tk.StringVar(value="正常战斗模式")  # 默认选中 normal mode
        self.weather_var = tk.StringVar(value="正常天气")  # 默认天气为晴天
        self.weather_menu = tk.OptionMenu(
            self.tournament_battle_frame,
            self.weather_var,  # 绑定天气变量
            "正常天气", "重力太空", "极热沙漠", "暗黑界域", "海洋之星", "藤蔓之眼", "光明城堡", "雷霆风暴", "众生平等",
            command=self.on_weather_change  # 回调函数
        )
        self.weather_menu.grid(row=0, column=0, padx=10, pady=10)
        self.normal_button = tk.Radiobutton(self.tournament_battle_frame, text="正常战斗模式", variable=self.mode_var,
                                            value="正常战斗模式",
                                            command=self.on_mode_change)
        self.clone_button = tk.Radiobutton(self.tournament_battle_frame, text="克隆模式", variable=self.mode_var,
                                           value="克隆模式",
                                           command=self.on_mode_change)
        self.normal_button.grid(row=0, column=1, padx=5, pady=10, sticky="e")
        self.clone_button.grid(row=0, column=2, padx=5, pady=10, sticky="e")
        self.back_button = tk.Button(self.tournament_battle_frame, text="返回", command=self.return_to_main1, font=("Arial", 14))
        self.back_button.grid(row=0, column=3, padx=5, pady=10, sticky="e")
        self.attribute_label_tournament = tk.Label(self.tournament_battle_frame, text="选择属性进行积分赛", font=("Arial", 14))
        self.attribute_label_tournament.grid(row=1, column=0, pady=2, columnspan=1)
        self.attribute_listbox_tournament = tk.Listbox(self.tournament_battle_frame, height=6, width=20, selectmode=tk.SINGLE)
        self.attribute_listbox_tournament.grid(row=2, column=0, pady=10, columnspan=2)
        shuxinglist=list(self.attribute_groups.keys())
        shuxinglist.append('全体')
        print(shuxinglist)
        for attribute in shuxinglist:
            self.attribute_listbox_tournament.insert(tk.END, attribute)
        self.canvas = tk.Canvas(self.tournament_battle_frame)
        self.scrollbar = tk.Scrollbar(self.tournament_battle_frame, orient="vertical", command=self.canvas.yview)
        self.hscrollbar = tk.Scrollbar(self.tournament_battle_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.config(yscrollcommand=self.scrollbar.set, xscrollcommand=self.hscrollbar.set)
        self.result_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.result_frame, anchor="nw")
        self.canvas.grid(row=3, column=0, sticky="nsew", columnspan=4)
        self.scrollbar.grid(row=3, column=2, sticky="ns", columnspan=3)
        self.hscrollbar.grid(row=4, column=0, sticky="ew", columnspan=3)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.result_label = tk.Label(self.result_frame, text="比赛结果将在此显示...", font=("Arial", 12))
        self.result_label.grid(row=0, column=0, pady=10)
        self.start_tournament_battle_button = tk.Button(self.tournament_battle_frame, text="开始对战", command=self.start_tournament_battle, font=("Arial", 14))
        self.start_tournament_battle_button.grid(row=1, column=2, pady=20, columnspan=2)
        self.tournament_battle_frame.grid_rowconfigure(0, weight=0)  # 第一行（按钮区域）
        self.tournament_battle_frame.grid_rowconfigure(1, weight=0)  # 第二行（属性标签）
        self.tournament_battle_frame.grid_rowconfigure(2, weight=1)  # 属性选择框区域
        self.tournament_battle_frame.grid_rowconfigure(3, weight=1)  # 滚动框区域
        self.tournament_battle_frame.grid_rowconfigure(4, weight=0)  # 水平滚动条
        self.tournament_battle_frame.grid_rowconfigure(5, weight=0)  # 开始按钮
        self.tournament_battle_frame.grid_columnconfigure(0, weight=1)  # 列1，按钮和选择框
        self.tournament_battle_frame.grid_columnconfigure(1, weight=1)  # 列2，按钮和选择框
        self.tournament_battle_frame.grid_columnconfigure(2, weight=0)  # 列3，按钮和滚动条
    def on_mouse_wheel(self, event):
        """响应鼠标滚轮事件进行滚动"""
        if event.delta:  # 对于不同操作系统的兼容性处理
            direction = -1 if event.delta > 0 else 1
            self.canvas.yview_scroll(direction, "units")
    def on_mouse_wheel1(self, event):
        """响应鼠标滚轮事件进行滚动"""
        if event.delta:  # 对于不同操作系统的兼容性处理
            direction = -1 if event.delta > 0 else 1
            self.canvas1.yview_scroll(direction, "units")
    def return_to_mainn(self):
        """返回主界面"""
        self.bai_frame.pack_forget()
        write_log("退出百宝箱界面，返回主界面")
        self.main_frame.pack(pady=50)
    def return_to_mainn2(self):
        """返回主界面"""
        self.log_frame.pack_forget()
        write_log("关闭日志功能，返回百宝箱界面")
        self.bai_frame.pack(pady=50)
    def return_to_mainn1(self):
        """返回主界面"""
        self.version_control_window.pack_forget()
        write_log("关闭版本控制功能，返回百宝箱界面")
        self.bai_frame.pack(pady=50)
    def return_to_main(self):
        """返回主界面"""
        self.single_battle_frame.pack_forget()
        write_log('退出单挑模式，回到主界面')
        self.main_frame.pack(pady=50)
    def return_to_main1(self):
        """返回主界面"""
        self.tournament_battle_frame.pack_forget()
        write_log('退出积分赛模式界面，返回主界面')
        self.main_frame.pack(pady=50)
    def return_to_main_2(self):
        """返回主界面"""
        self. feature_battle_frame.pack_forget()
        write_log('退出属性大战模式界面，返回主界面')
        self.main_frame.pack(pady=50)
    def return_to_main_3(self):
        """返回主界面"""
        self.paiming_frame.pack_forget()
        write_log('退出排名界面，返回主界面')
        self.main_frame.pack(pady=50)

    def return_to_main_4(self):
        """返回主界面"""
        self.shijiesai_frame.pack_forget()
        write_log('退出世界赛界面，返回主界面')
        self.main_frame.pack(pady=50)
    def return_to_main2(self):
        """返回主界面"""
        self.elimination_battle_frame.pack_forget()
        write_log('退出淘汰赛模式界面，返回主界面')
        self.main_frame.pack(pady=50)
    def return_to_main3(self):
        """返回主界面"""
        self.training_battle_frame.pack_forget()
        write_log('退出团队历练模式界面，返回历练模式界面')
        self.training_frame.pack(pady=50)
    def return_to_main4(self):
        """返回主界面"""
        self.sig_training_battle_frame.pack_forget()
        write_log('退出个人历练模式界面，返回历练模式界面')
        self.training_frame.pack(pady=50)
    def return_to_main5(self):
        """返回主界面"""
        self.training_frame.pack_forget()
        write_log('退出历练模式界面，返回主界面')
        self.main_frame.pack(pady=50)
    def update_pokemon_list1(self, event):
        """更新宝可梦列表框，根据选择的属性显示宝可梦"""
        self.shuru=0
        selected_attribute1 = self.attribute_listbox1.get(tk.ACTIVE)
        pokemons_of_attribute1 = self.attribute_groups[selected_attribute1]
        self.selected_pokemon1_shuxing = selected_attribute1
        self.pokemon_listbox1.delete(0, tk.END)
        for pokemon in pokemons_of_attribute1:
            self.pokemon_listbox1.insert(tk.END, pokemon.name)
    def update_pokemon_list3(self, event):
        """更新宝可梦列表框，根据选择的属性显示宝可梦"""
        try:
            selected_attribute = self.attribute_listboxq_1.get(tk.ACTIVE)
            if selected_attribute is None:
                messagebox.showwarning("选择错误", "请从属性列表中选择一个属性！")
                return
            shuxing = None
            eligible_pokemons=None
            if selected_attribute == '全体':
                shuxing = '全体'
                eligible_pokemons = self.pokemons
            elif selected_attribute == '精英':
                shuxing = '精英'
                eligible_pokemons = load_pokemons_from_file(file_path='全体jingying.txt')
            elif selected_attribute.endswith("系精英"):
                shuxing = selected_attribute[:-3]
                print(shuxing)
                eligible_pokemons = load_pokemons_from_file(file_path=shuxing + 'jingying' + '.txt')
            else:
                shuxing = selected_attribute
                eligible_pokemons = self.attribute_groups[selected_attribute]
            self.lilian_pokemon_shuxing = shuxing
            pokemons_of_attribute1 = eligible_pokemons
            self.lilian_pokemon_list=eligible_pokemons
            self.pokemon_listboxq_1.delete(0, tk.END)
            for pokemon in pokemons_of_attribute1:
                self.pokemon_listboxq_1.insert(tk.END, pokemon.name)
        except FileNotFoundError:
            messagebox.showwarning("选择错误", "对应文件不存在，请先进行淘汰赛生成文件！")
    def update_pokemon_list2(self, event):
        self.shuru = 0
        """更新宝可梦列表框，根据选择的属性显示宝可梦"""
        selected_attribute2 = self.attribute_listbox2.get(tk.ACTIVE)
        pokemons_of_attribute2 = self.attribute_groups[selected_attribute2]
        self.selected_pokemon2_shuxing = selected_attribute2
        self.pokemon_listbox2.delete(0, tk.END)
        for pokemon in pokemons_of_attribute2:
            self.pokemon_listbox2.insert(tk.END, pokemon.name)
    def start_battle1(self):
        """选择宝可梦1"""
        global selected1_idx
        try:
            if(self.shuru==0):
                selected1_idx = self.pokemon_listbox1.curselection()[0]
                self.selected_pokemon1 = self.attribute_groups[self.selected_pokemon1_shuxing][selected1_idx]
                write_log(f"选定单挑模式宝可梦1为    {self.selected_pokemon1.name}")
                messagebox.showwarning("选择成功",f"宝可梦1为    {self.selected_pokemon1.name}")
            else:
                self.selected_pokemon1 = [pokemon for pokemon in self.pokemons if pokemon.name == self.name][0]
                print(self.selected_pokemon1)
                messagebox.showwarning("选择成功",f"宝可梦1为    {self.selected_pokemon1.name}")
        except IndexError:
            messagebox.showwarning("选择错误", "宝可梦1未选择！")
    def start_battle3(self):
        """选择宝可梦1"""
        global selected3_idx
        try:
            selected3_idx = self.pokemon_listboxq_1.curselection()[0]
            print(self.lilian_pokemon_shuxing)
            print(selected3_idx)
            self.lilian_pokemon = self.lilian_pokemon_list[selected3_idx]
            print(self.lilian_pokemon.name)
            write_log(f"选定个人历练模式宝可梦为    {self.lilian_pokemon.name}")
            messagebox.showwarning("选择成功",f"历练宝可梦为    {self.lilian_pokemon.name}")
        except IndexError:
            messagebox.showwarning("选择错误", "历练宝可梦未选择！")
    def start_battle2(self):
        """选择宝可梦2"""
        global selected2_idx
        try:
            if (self.shuru == 0):
                selected2_idx = self.pokemon_listbox2.curselection()[0]
                self.selected_pokemon2 = self.attribute_groups[self.selected_pokemon2_shuxing][selected2_idx]
                write_log(f"选定单挑模式宝可梦2为    {self.selected_pokemon2.name}")
                messagebox.showwarning("选择成功", f"宝可梦2为    {self.selected_pokemon2.name}")
            else:
                self.selected_pokemon2 = [pokemon for pokemon in self.pokemons if pokemon.name == self.name][0]
                print(self.selected_pokemon2)
                messagebox.showwarning("选择成功", f"宝可梦2为    {self.selected_pokemon2.name}")
        except IndexError:
            messagebox.showwarning("选择错误", "宝可梦2未选择！")
    def delete(self,canvas):
        canvas.delete("all")
    def start_battle(self):
        write_log('两只宝可梦开始单挑')
        try:
            self.selected_pokemon1.total_points = random.randint(9, 15)  # 随机点数
            self.selected_pokemon2.total_points = random.randint(9, 15)  # 随机点数
            pokemon1=self.selected_pokemon1
            pokemon2 = self.selected_pokemon2
            pokemon1_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                 pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2, pokemon1.weaknesses,
                                 pokemon1.resistances, pokemon1.skill1type, pokemon1.skill2type, pokemon1.total_points)
            pokemon2_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1,
                                 pokemon2.skill2, pokemon2.special_skill1, pokemon2.special_skill2, pokemon2.weaknesses,
                                 pokemon2.resistances, pokemon2.skill1type, pokemon2.skill2type, pokemon2.total_points)
            text1 = "对战开始！  \n"
            text1+=f"{pokemon1_1.name} VS {pokemon2_2.name}   \n"
            text1 += f"{pokemon1_1}    \n"
            text1 += f"{pokemon2_2}    \n"
            result,result1 ,result_3= battle(pokemon1_1, pokemon2_2,self.moshi,self.whehter)
            for i in result1:
                text1+=i+ "  \n"
            self.display_battle_output(text1)
            write_log(result)
            messagebox.showinfo("对战结果", f"对战结束！\n结果: {result}")
        except IndexError:
            messagebox.showwarning("选择错误", "请从每个列表框中选择一只宝可梦！")
    def start_tournament_battle(self):
        """开始积分赛对战"""
        try:
            LB=1
            start_time=time.time()
            selected_attribute = self.attribute_listbox_tournament.get(tk.ACTIVE)
            write_log(f"选择：  {selected_attribute}  成员进行积分赛测试")
            print(selected_attribute)
            pokemon_list=None
            rounds = self.get_rounds_from_user()
            P_LIST=None
            if rounds is not None:
                if(rounds>len(self.pokemons)):
                    rounds=len(self.pokemons)
                write_log(f"本次积分赛取前：  {rounds}  名进行展示")
                if(selected_attribute=='全体'):
                    pokemon_list =self.pokemons
                    LB=1
                else:
                    LB=2
                    pokemon_list=self.attribute_groups[selected_attribute]
                for i in pokemon_list:
                    i.useskill=self.useskilltable[i.name]
            P_LIST=round_robin_tournament(pokemon_list, rounds, self.moshi, self.whehter)
            end_time = time.time()
            self.display_ranking(P_LIST, rounds, selected_attribute)
            sorted_pokemons = sorted(P_LIST, key=self.ranking_key)
            for rank, pokemon in enumerate(sorted_pokemons[:rounds], start=1):
                if(LB==1):
                    pokemon.person_score+=(len(sorted_pokemons)+1-rank)*3
                if (LB == 2):
                    pokemon.person_score += (len(sorted_pokemons) + 1 - rank) * 2
            for rank, pokemon in enumerate(sorted_pokemons[:rounds], start=1):
                self.rank_system.update_pokemon_rank(pokemon)
            save_rank_data(self.rank_system)
            # 保存到文件
            elapsed_time = end_time - start_time
            messagebox.showinfo("运行时间  ", str(elapsed_time) + "  秒")
        except IndexError:
            messagebox.showwarning("选择错误", "请从属性列表中选择一个属性！")
    def get_rounds_from_user(self):
        """通过弹窗获取用户输入的轮次数"""
        rounds = simpledialog.askinteger("输入参数", "请输入取积分前几名：", minvalue=1)
        if rounds is None:
            messagebox.showwarning("输入错误", "请输入有效的参数！")
            return None
        return rounds
def rank_data(pokemon):
    rank_system = Rank()
    for i in pokemons:
        rank_system.add_pokemon(i)
    rank_system.update_pok_rank()
    with open('rank.txt', "w", encoding="utf-8") as f:
        f.write("个人排名:\n")
        COUNT = 1
        for name, score in rank_system.pokemon_rankings.items():
            f.write(f"{name} -个人排名: {COUNT} -得分: {score}\n")
            COUNT += 1
        f.write("\n2人团体排名:\n")
        COUNT = 1
        for name, score in rank_system.team2_rankings.items():
            f.write(f"{name} -团队排名: {COUNT} - 团队成员: {score.namelist} - 团队得分: {score.team_score}\n")
            COUNT += 1
        f.write("\n3人团体排名:\n")
        COUNT = 1
        for name, score in rank_system.team3_rankings.items():
            f.write(f"{name} -团队排名: {COUNT} - 团队成员: {score.namelist} - 团队得分: {score.team_score}\n")
            COUNT += 1
        f.write("\n5人团体排名:\n")
        COUNT = 1
        for name, score in rank_system.team5_rankings.items():
            f.write(f"{name} -团队排名: {COUNT} - 团队成员: {score.namelist} - 团队得分: {score.team_score}\n")
            COUNT += 1
        f.write("\n7人团体排名:\n")
        COUNT = 1
        for name, score in rank_system.team7_rankings.items():
            f.write(f"{name} -团队排名: {COUNT} - 团队成员: {score.namelist} - 团队得分: {score.team_score}\n")
            COUNT += 1
def save_rank_data(rank_system):
    with open('rank.txt', "w", encoding="utf-8") as f:
        f.write("个人排名:\n")
        COUNT = 1
        for name, score in rank_system.pokemon_rankings.items():
            f.write(f"{name} -个人排名: { COUNT} -得分: {score}\n")
            COUNT += 1
        f.write("\n2人团体排名:\n")
        COUNT = 1
        for name, score in rank_system.team2_rankings.items():
            f.write(f"{name}  -团队排名: {COUNT} - 团队成员: {score.namelist} - 团队得分: {score.team_score}\n")
            COUNT += 1
        f.write("\n3人团体排名:\n")
        COUNT = 1
        for name, score in rank_system.team3_rankings.items():
            f.write(f"{name}  -团队排名: {COUNT} - 团队成员: {score.namelist} - 团队得分: {score.team_score}\n")
            COUNT += 1
        f.write("\n5人团体排名:\n")
        COUNT = 1
        for name, score in rank_system.team5_rankings.items():
            f.write(f"{name}  -团队排名: {COUNT} - 团队成员: {score.namelist} - 团队得分: {score.team_score}\n")
            COUNT += 1
        f.write("\n7人团体排名:\n")
        COUNT = 1
        for name, score in rank_system.team7_rankings.items():
            f.write(f"{name}  -团队排名: {COUNT} - 团队成员: {score.namelist} - 团队得分: {score.team_score}\n")
            COUNT += 1
def load_rank_from_txt(pokemons):
    rank_system = Rank()  # 创建Rank对象
    with open('rank.txt', "r", encoding="utf-8") as f:
        content = f.read().split("\n")  # 按行读取文件内容
    section = None  # 用来标记当前解析的部分
    for line in content:
        line = line.strip()
        if line == "个人排名:":
            section = "pokemon"
            continue
        elif line == "2人团体排名:":
            section = "team"
            continue
        elif line == "3人团体排名:":
            section = "team"
            continue
        elif line == "5人团体排名:":
            section = "team"
            continue
        elif line == "7人团体排名:":
            section = "team"
            continue
        if section == "pokemon" and line:
            name, score = line.split(" -得分: ")
            na, pm = line.split(" -个人排名: ")
            rank_system.pokemon_rankings[na] = int(score)
        elif section == "team" and line:
            na, rest = line.split(" - 团队得分: ")
            members_str = rest.split(" - 团队成员: ")[0]  # 获取得分
            nam,members = na.split(" - 团队成员: ") # 解析成员列表
            name, count = nam.split("  -团队排名: ")  # 解析成员列表
            team_members = ast.literal_eval(members)
            team = []
            for member in team_members:
                matched_pokemon = next((p for p in pokemons if p.name == member), None)
                if matched_pokemon:
                    team.append(matched_pokemon)
            team1 = T_EAM(name, team )  # 2人团队
            team1.team_score= int(members_str.strip())
            rank_system.add_team(team1, team_size=len(team1.members))
    rank_system.pokemon_rankings = dict(sorted(rank_system.pokemon_rankings.items(), key=lambda x: x[1], reverse=True))
    rank_system.team2_rankings = dict(sorted(rank_system.team2_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
    rank_system.team3_rankings = dict(sorted(rank_system.team3_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
    rank_system.team5_rankings = dict(sorted(rank_system.team5_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
    rank_system.team7_rankings = dict(sorted(rank_system.team7_rankings.items(), key=lambda x: x[1].team_score, reverse=True))
    rank_system.team2_names = list(rank_system.team2_rankings.keys())
    rank_system.team3_names = list(rank_system.team3_rankings.keys())
    rank_system.team5_names = list(rank_system.team5_rankings.keys())
    rank_system.team7_names = list(rank_system.team7_rankings.keys())
    for i in pokemons:
        i.person_score = rank_system.pokemon_rankings[i.name]
    return rank_system  # 返回初始化的rank_system对象
def load_or_initialize_most_used_skills(file_path, pokemons,GGGG):
    useskill_table = {}
    # 尝试加载文件
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                # print(line)
                name, skill = line.strip().split(": ")
                # print(skill)
                useskill_table[name] = skill if skill != "None" else None
                if (skill == "None"):
                    GGGG=1
    else:
        GGGG=1
        # 文件不存在，初始化为None
        with open(file_path, "w", encoding="utf-8") as file:
            for pokemon in pokemons:
                file.write(f"{pokemon.name}:None\n")
                useskill_table[pokemon.name] = None
    return useskill_table,GGGG
def round_robin_challenge(pokemon_list, useskilltable):

    # 随机打乱宝可梦列表
    random.shuffle(pokemon_list)
    minround=100000
    plist=None
    no_update_count = 0  # 计数器，记录未更新回合数
    for i in pokemon_list:
        i.useskill= useskilltable[i.name]
    while True:
        # 本轮挑战成功的次数
        round_successful_challenges = 0
        # 每一轮挑战，从列表的最后一位开始向前挑战
        for i in range(len(pokemon_list) - 1, 0, -1):  # 从列表的最后一位开始向前挑战
            pokemon1 = pokemon_list[i]#挑战者
            pokemon2 = pokemon_list[i - 1]#防守者

            pokemon1_1 = Pokemon(pokemon1.name, pokemon1.health, pokemon1.attribute, pokemon1.skill1,
                                 pokemon1.skill2, pokemon1.special_skill1, pokemon1.special_skill2,
                                 pokemon1.weaknesses, pokemon1.resistances, pokemon1.skill1type,
                                 pokemon1.skill2type, pokemon1.total_points)
            pokemon2_2 = Pokemon(pokemon2.name, pokemon2.health, pokemon2.attribute, pokemon2.skill1,
                                 pokemon2.skill2, pokemon2.special_skill1, pokemon2.special_skill2,
                                 pokemon2.weaknesses, pokemon2.resistances, pokemon2.skill1type,
                                 pokemon2.skill2type, pokemon2.total_points)
            # pokemon1_1.useskill = pokemon1.useskill
            # pokemon2_2.useskill = pokemon2.useskill
            result, result1, result_2 = battle(pokemon1_1, pokemon2_2, "正常模式", "正常天气")
            if result == f"{pokemon1_1.name} 胜利":#挑战者胜利
                round_successful_challenges += 1
                pokemon_list[i], pokemon_list[i - 1] = pokemon_list[i - 1], pokemon_list[i]
 # 如果当前回合的挑战成功次数少于之前的最小次数，更新最小挑战次数和宝可梦列表
        if minround >= round_successful_challenges:
            minround = round_successful_challenges
            plist = pokemon_list
            no_update_count = 0  # 重置计数器，因为有更新
        else:
            no_update_count += 1  # 未更新，计数器加1

        print(round_successful_challenges, minround,no_update_count)

        # 如果最小挑战成功次数小于 5，或者超过 100 回合没有更新，退出循环
        if minround < 2 or no_update_count >= 500:
            for pokemon in pokemon_list:
                print(pokemon.name)
            break

    # 返回当前最优的宝可梦列表
    return plist

def save_damage_to_txt(pokemons, useskilltable, filename='C://Users\zuoshangkun\PycharmProjects\BKM\damage_data.txt'):
    # print( useskilltable)
    with open(filename, 'w') as f:
        for i in pokemons:
            # 计算最小和最大伤害
            print(i.name)
            damage1 = getattr(i, useskilltable[i.name])[0] * int(9 / getattr(i, useskilltable[i.name])[1])  # 最小伤害
            damage2 = getattr(i, useskilltable[i.name])[0] * int(15 / getattr(i, useskilltable[i.name])[1])  # 最大伤害
            # 写入文件，每行存储宝可梦的名字及对应的最小和最大伤害
            f.write(f"{i.name}: {damage1},{damage2}\n")
    print(f"数据已保存到 {filename}")
def load_damage_from_txt(filename='damage_data.txt'):
    damage_dict = {}
    with open(filename, 'r') as f:
        for line in f:
            # 解析每行数据
            name, damages = line.strip().split(": ")
            min_damage, max_damage = map(int, damages.split(","))
            damage_dict[name] = {'min_damage': min_damage, 'max_damage': max_damage}
    return damage_dict



pokemons = load_pokemons_from_file()
GGGG=0
useskilltable, GGGG = load_or_initialize_most_used_skills("C://Users//zuoshangkun\PycharmProjects\BKM\most_used_skills.txt", pokemons, GGGG)
# for i in pokemons:
#     damage1 = getattr(i, useskilltable[i.name])[0] * int(9 / getattr(i, useskilltable[i.name])[1])  # 获得伤害
#     damage2 = getattr(i, useskilltable[i.name])[0] * int(15 / getattr(i, useskilltable[i.name])[1])  # 获得伤害
#     print(i.name, damage1, damage2)

save_damage_to_txt(pokemons, useskilltable)
damage_dict = load_damage_from_txt()
round_robin_tournament(pokemons, 300, "正常战斗模式", "正常天气")
# if __name__ == "__main__":
#     write_log("运行程序")
#     if not os.path.exists('pokemons.txt'):
#         generate_and_save_pokemon_data()
#         write_log("当前路径下不存在 pokemons.txt 文件，进行随机生成")
#     file_path = "readme.txt"
#     if os.path.exists(file_path):
#         with open(file_path, "r", encoding="utf-8") as file:
#             file_content = file.read()
#         messagebox.showinfo("版本更新内容  ", file_content)
#     pokemons = load_pokemons_from_file()
#     p1=[]
#     for i in pokemons:
#         if i.attribute=="暗":
#             p1.append(i)
#
#     health_table=load_pokemons_from_file1()
#     # print(health_table)
#
#     # round_robin_challenge(pokemons)
#     # 运行遗传算法
#
#     if not os.path.exists('rank.txt'):
#         rank_data(pokemons)
#         write_log("当前路径下不存在 rank.txt 文件，进行随机生成")
#     useskilltable,GGGG=load_or_initialize_most_used_skills("most_used_skills.txt", pokemons,GGGG)
#     for i in pokemons:
#         damage1= getattr(i, useskilltable[i.name])[0] *int(9/getattr(i, useskilltable[i.name])[1]) # 获得伤害
#         damage2 = getattr(i, useskilltable[i.name])[0] * int(15 / getattr(i, useskilltable[i.name])[1])  # 获得伤害
#         print(i.name  , damage1,damage2)
#
#     save_damage_to_txt(pokemons, useskilltable)
#
#     # 从文件中读取数据
#     damage_dict = load_damage_from_txt()
#    # // print(int(damage_dict["电·皮卡丘"]['min_damage']))
#    #  round_robin_challenge( p1,useskilltable)
#     rank_system =load_rank_from_txt(pokemons)
#     root = tk.Tk()
#     app = PokemonBattleApp(root, pokemons,rank_system,useskilltable)
#     root.mainloop()
