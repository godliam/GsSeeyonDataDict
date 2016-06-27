#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Liam0611'

import pymssql
import xml.etree.ElementTree as Etree
from getCode import getCode


class GsSeeyonDataDict:
    def getModuleDataDict(self, moduleName):
        if not moduleName:
            return None

        sqlStr = r"SELECT FIELD_INFO FROM FORM_DEFINITION " \
                 r"WHERE NAME = '{moduleName}'".format(moduleName=moduleName)
        self.__dbCursor.execute(sqlStr)
        resXmlStr = self.__dbCursor.fetchall()

        xmlRoot = Etree.fromstring(resXmlStr[0][0])

        resDataDict = {}

        # Reading by xml.
        for tables in xmlRoot:
            tableInfo = tables.attrib
            tableInfo['display'] = getCode(tableInfo['display'], 'gb2312')
            filedDataDict = {}
            filedDataDict['TableName'] = tableInfo['name']
            for fields in tables.find('FieldList'):
                fieldInfo = fields.attrib
                filedDataDict[getCode(fieldInfo['display'], 'gb2312')] = fieldInfo['name']
            if r'master' == tableInfo['tabletype']:
                resDataDict[moduleName] = filedDataDict
            else:
                resDataDict[tableInfo['display']] = filedDataDict

        return resDataDict

    def getAllModuleDataDict(self):
        sqlStr = r"SELECT NAME FROM FORM_DEFINITION"
        self.__dbCursor.execute(sqlStr)
        resDataDicts = {}
        for moduleName in self.__dbCursor.fetchall():
            resDataDicts[moduleName[0]] = self.getModuleDataDict(moduleName[0])

        return resDataDicts

    def __init__(self, host, user, password, database):
        self.__dbConn = pymssql.connect(host=host, user=user, password=password, database=database, charset='utf8')
        self.__dbCursor = self.__dbConn.cursor()

    def __del__(self):
        try:
            self.__dbConn.close()
        except:
            pass


if __name__ == '__main__':
    gsDataDict = GsSeeyonDataDict(host='', user='', password='', database='')

    allDataDict = gsDataDict.getAllModuleDataDict()
    print(allDataDict)
