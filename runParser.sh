#!/bin/bash
for %f in (ebay_data\*.json) do python my_ebay_parser.py %f

#PowerShell Commands

Get-Content PREMEMBER.dat | sort | unique | Out-File -encoding UTF8 MEMBER.dat
Get-Content PREITEM.dat | sort | unique | Out-File -encoding UTF8 ITEM.dat
Get-Content PREITEMCATEGORY.dat | sort | unique | Out-File -encoding UTF8 ITEMCATEGORY.dat
Get-Content PREBID.dat | sort | unique | Out-File -encoding UTF8 BID.dat
Get-Content PRECATEGORY.dat | sort | unique | Out-File -encoding UTF8 CATEGORY.dat
