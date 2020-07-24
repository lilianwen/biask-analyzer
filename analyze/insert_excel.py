import xlwt
f = xlwt.Workbook() #创建工作簿
sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
l_=[1,2,3,4,5]
for i in range(len(l_)):
    sheet1.write(0,i)#表格的第一行开始写。第一列，第二列。。。。 
#sheet1.write(0,0,start_date,set_style('Times New Roman',220,True))
f.save('text.xls')#保存文件