import csv
import urllib.request
import random
import heapq
from flask import Flask, render_template, escape, request, redirect
import pandas as pd
import ssl
from enum import Enum

ssl._create_default_https_context = ssl._create_unverified_context


class StudentProfile:
    req_sat_score = 0
    uni_tuition_fee = 0

    def __init__(self, req_sat_score, uni_tuition_fee):
        self.req_sat_score = req_sat_score
        self.uni_tuition_fee = uni_tuition_fee

# Defining model clas for univeristy information


class Info_Of_Uni:
    uni_rank = 0
    uni_city = ''
    uni_state = ''
    uni_tuition_fee = 0
    req_sat_score = 0
    uni_acceptance_rate = 0
    t_debt = 0
    ratio_of_male = 0

    def __init__(self, uni_rank, uni_city, uni_state, uni_tuition_fee, req_sat_score, uni_acceptance_rate, t_debt, ratio_of_male):
        self.uni_rank = uni_rank
        self.uni_city = uni_city
        self.uni_state = uni_state
        self.uni_tuition_fee = uni_tuition_fee
        self.req_sat_score = req_sat_score
        self.uni_acceptance_rate = uni_acceptance_rate
        self.t_debt = t_debt
        self.ratio_of_male = ratio_of_male

    def ToString(self):
        return self.uni_city + '\t' + self.uni_state + '\t' + str(self.uni_rank) + '\t' + str(self.uni_tuition_fee) + '\t' + str(self.req_sat_score) + '\t' + str(self.uni_acceptance_rate) + '\t' + str(self.t_debt) + '\t' + str(self.ratio_of_male)

    def ToStringWithName(self):
        return 'city:' + self.uni_city + '\tstate:' + self.uni_state + '\trank:' + str(self.uni_rank) + '\ttuition:' + str(self.uni_tuition_fee) + '\tsat:' + str(self.req_sat_score) + '\tAC:' + str(self.uni_acceptance_rate) + '\tdebt:' + str(self.t_debt) + '\tMal:' + str(self.ratio_of_male)

# cleaning function will give selected required columns as output


def cleaning_fn(df, attributes):
    input_reader = open(df)
    inputFile = csv.DictReader(input_reader)
    output = {}
    for key in attributes:
        output[key] = []
    for row in inputFile:
        for key in attributes:
            if key in row.keys():
                output[key].append(row[key])
    input_reader.close()
    return output


def takingUserInput():

    while True:
        direct_input1 = request.args.get("sat")
        try:
            input2 = float(direct_input1)
        except Exception as ex:
            continue
        break
    while True:
        direct_input2 = request.args.get("tution")
        try:
            input3 = float(direct_input2)
        except Exception as ex:
            continue
        break
    return StudentProfile(input2, input3)


def finding_rank_ofUni():
    url_of_uni_rankings = "http://www.4icu.org/us/"
    url_handler = urllib.request.urlopen(url_of_uni_rankings)
    html = url_handler.read()
    html = html.decode("utf8")
    output = {}
    uni_location = 0
    resulting_rank = 0
    while True:
        try:
            uni_location1 = html.index('.htm">', uni_location)
            print(uni_location1)
            uni_location2 = html.index('</a>', uni_location1)
            print(uni_location2)
            output[html[(uni_location1 + len('.htm">')): uni_location2]] = resulting_rank
            resulting_rank += 1
            uni_location = uni_location2 + 1
        except Exception as ex:
            print(ex)
            break
    return output


def ProcessFinalData(df, ranking_of_uni):
    no_of_rows = len(df['INSTNM'])
    output = {}
    for i in range(no_of_rows):
        uni_name = df['INSTNM'][i]
        if uni_name not in ranking_of_uni:
            continue
        uni_rank = ranking_of_uni[uni_name]
        uni_city = df['CITY'][i]
        uni_state = df['STABBR'][i]
        try:
            uni_tuition_fee = float(df['TUITIONFEE_OUT'][i])
            req_sat_score = float(df['SAT_AVG_ALL'][i])
            uni_acceptance_rate = float(df['ADM_RATE_ALL'][i])
            uni_tuition_fee = float(df['TUITIONFEE_OUT'][i])
            t_debt = float(df['DEBT_MDN_SUPP'][i])
            ratio_of_male = float(df['UGDS_MEN'][i])
            output[uni_name] = Info_Of_Uni(
                uni_rank, uni_city, uni_state, uni_tuition_fee, req_sat_score, uni_acceptance_rate, t_debt, ratio_of_male)
        except Exception as ex:
            pass
    return output


def filteration_of_uni(profile_of_user, data):
    output = {}
    for (i, j) in data.items():
        if profile_of_user.req_sat_score >= j.req_sat_score and profile_of_user.uni_tuition_fee >= j.uni_tuition_fee:
            output[i] = j
    return output


def dataNormalizationFun(data):

    max_normalization = max(data)
    min_normalization = min(data)

    output = []
    for i in data:
        if (max_normalization == min_normalization):
            output.append(1)
        else:
            output.append((i - min_normalization)*1.0 /
                          (max_normalization - min_normalization))
    return output


def get_toplist_of_uni(data, score, N):
    topUniversities = sorted(score.items(), key=lambda x: -x[1])[:5]
    return topUniversities


def generating_recommendation_uni(data_for_recommendation):
    uni_names = []
    sat_scores = []
    tuition_fees = []
    uni_rankings = []
    uni_acceptance_rate = []

    for (i, j) in data_for_recommendation.items():
        uni_names.append(i)
        tuition_fees.append(j.uni_tuition_fee)
        sat_scores.append(j.req_sat_score)
        uni_acceptance_rate.append(j.uni_acceptance_rate)
        uni_rankings.append(j.uni_rank)
    tuition_fees = dataNormalizationFun(tuition_fees)
    uni_rankings = dataNormalizationFun(uni_rankings)
    sat_scores = dataNormalizationFun(sat_scores)

    list_of_scores = {}
    for i in range(len(uni_names)):
        list_of_scores[uni_names[i]] = 0.15 * (1 - tuition_fees[i]) + 0.4 * \
            (1 - sat_scores[i]) + 0.35 * \
            uni_acceptance_rate[i] + 0.2*(1-uni_rankings[i])
    generated_recommendations = get_toplist_of_uni(
        data_for_recommendation, list_of_scores, 5)
    return generated_recommendations


def main():
    # extracting the specific number of columns needed using column names
    extracted_user_data = cleaning_fn('C:/Users/mnkgr/OneDrive/Desktop/University Recommendation System/datasets/MERGED2016_17_PP.csv', [
        'INSTNM', 'CITY', 'STABBR', 'TUITIONFEE_OUT',  'SAT_AVG_ALL', 'ADM_RATE_ALL', 'DEBT_MDN_SUPP', 'UGDS_MEN'])

    search_uni_rank = finding_rank_ofUni()
    data_finalized = ProcessFinalData(extracted_user_data, search_uni_rank)

    while True:
        generating_user_profile = takingUserInput()
        data_filteration_process = filteration_of_uni(
            generating_user_profile, data_finalized)

        if len(data_filteration_process) == 0:
            continue

        else:
            recommended_result = generating_recommendation_uni(
                data_filteration_process)

        print("Result in college", recommended_result)
        return recommended_result


if __name__ == "__main__":
    main()
