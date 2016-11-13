# coding:gbk
import wx
import wx.grid
import GenericTable
from SQL_test import MySQLTest


class BaseInfoOfStudentPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        self.sqlstament = MySQLTest()
        self.table_name = u'ѧ��������Ϣ'
        self.select_item_list = [u'*', u'ѧ��', u'����', u'��ͥסַ', u'�Ա�', u'����', u'�������']
        super(BaseInfoOfStudentPanel, self).__init__(*args, **kwargs)
        title_font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)  # ��������
        self.gbsizer = wx.GridBagSizer(hgap=10, vgap=10)
        self.second_panel = wx.Panel(self, size=(238, 270), pos=(600, 100),
                                     style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)

        self.title_label = wx.StaticText(self, label=u"ѧ��������Ϣ����", pos=(308, 10))
        select_item_label = wx.StaticText(self, label=u"��ѯ��:", pos=(10, 10))
        value_label = wx.StaticText(self, label=u"ֵ:", pos=(96, 10))
        self.title_label.SetFont(title_font)
        self.title_label.SetForegroundColour("#21c4c3")  # ����������ɫ

        self.SelectButton = wx.Button(self, label=u'��ѯ', pos=(144, 30), size=(33, 25))
        self.AddButton = wx.Button(self, label=u'����һ��', pos=(680, 8), size=(60, 25))
        self.DropButton = wx.Button(self, label=u'ɾ��һ��', pos=(680, 35), size=(60, 25))
        self.UpdateButton = wx.Button(self, label=u'�޸�����', pos=(740, 8), size=(60, 25))
        self.RefreshButton = wx.Button(self, label=u'ˢ��', pos=(740, 35), size=(60, 25))
        self.SelectButton.Bind(wx.EVT_BUTTON, self.query_info)
        self.DropButton.Bind(wx.EVT_BUTTON, self.delete_info)
        self.AddButton.Bind(wx.EVT_BUTTON, self.add_info)
        self.RefreshButton.Bind(wx.EVT_BUTTON, self.refresh)
        self.UpdateButton.Bind(wx.EVT_BUTTON, self.updata_info)


        self.select_items = wx.ComboBox(self, pos=(10, 30), size=(80, -1), choices=self.select_item_list,
                                        style=wx.CB_DROPDOWN)
        self.valueTextCtrl = wx.TextCtrl(self, value="", pos=(92, 30), size=(50, 25))
        self.test_grid('select * from ѧ��������Ϣ')

    def test_grid(self, sqlsta):
        import SqlUtil
        data = SqlUtil.query_data(sqlsta)
        col_label = ("ѧ��", "����", "��ͥ��ַ", "�Ա�", "����", "�������")
        self.testgrid = wx.grid.Grid(self, size=(880, 300), pos=(10, 60))
        row_label = []
        for i in range(len(data)):
            row_label.append(i+1)
        self.testgrid.baseModel = GenericTable.GenericTable(data, row_label, col_label)
        self.testgrid.SetTable(self.testgrid.baseModel)

    def refresh(self, event):
        self.testgrid.Destroy()
        self.test_grid('select * from ѧ��������Ϣ')

    def delete_info(self, event):
        stunum = "00000000"
        entry_dlg = wx.TextEntryDialog(self, u'����һ��\"ѧ��\"��ɾ��', u'����һ��ѧ��')
        if entry_dlg.ShowModal() == wx.ID_OK:
            stunum = entry_dlg.GetValue()
        entry_dlg.Destroy()
        if stunum:
            splited_stunum = stunum.split(' ')  # ��Ϊ�û������ѧ�ſ��ܴ��ո�,�����Ȱ��ַ����ո���,�ٽ�������.(�ָ��Ϊһ������)
        # ͬ����������ʱҲ���ո���зָ�.
            joined_stunum = ''.join(splited_stunum)  # ���ѷָ����ַ���ƴ��
            stunum = joined_stunum
        sqlsta = self.sqlstament.delete_info(self.table_name, u'ѧ��', '=', stunum)
        print sqlsta
        self.sqlstament.execute_statement(sqlsta)

    def add_info(self, event):
        stu_infos = ""
        entry_dlg = wx.TextEntryDialog(self, u'����һ��ѧ����Ϣ,��ȱ����Ϣ��0����', u'����һ����Ϣ')
        if entry_dlg.ShowModal() == wx.ID_OK:
            stu_infos = entry_dlg.GetValue()
        entry_dlg.Destroy()
        if stu_infos:
            splited_stu_info = stu_infos.split(' ')
            stunum = splited_stu_info[0]
            stuname = splited_stu_info[1]
            stu_adress = splited_stu_info[2]
            stusex = splited_stu_info[3]
            stuage = splited_stu_info[4]
            stusituation = splited_stu_info[5]
            sqlsta = self.sqlstament.insert_info(stunum, stuname, stu_adress, stusex, stuage, stusituation,
                                                 self.table_name)
            print sqlsta
            self.sqlstament.execute_statement(sqlsta)
        else:
            return stu_infos

    def query_info(self, event):
        self.testgrid.Destroy()
        word = self.select_items.GetSelection()
        select_item_value = self.select_items.GetItems()[word]
        value = self.valueTextCtrl.GetRange(0, 50)
        if select_item_value == u"����":
            sqlsta = self.sqlstament.select_info(self.table_name, select_item_value, '=', value, 666)
        else:
            sqlsta = self.sqlstament.select_info(self.table_name, select_item_value, '=', value, 333)
        print sqlsta
        self.test_grid(sqlsta)

    def updata_info(self, event):
        self.select_item_list2 = [u'����', u'��ͥסַ', u'�Ա�', u'����', u'�������']
        self.stunum_temp_label = wx.StaticText(self.second_panel, label=u"�޸Ķ���ѧ��:", pos=(0, 5))
        self.stunumvalues_temp = wx.TextCtrl(self.second_panel, size=(80, 25), pos=(82, 0))
        self.column_name_temp = wx.StaticText(self.second_panel, label=u"Ҫ�޸ĵ�����:", pos=(0, 30))
        self.select_items_temp = wx.ComboBox(self.second_panel, size=(80, 25), pos=(0, 50),
                                        choices=self.select_item_list2, style=wx.CB_DROPDOWN)
        self.change_value = wx.StaticText(self.second_panel, label=u'  �޸ĺ��ֵ:', pos=(82, 30))
        self.values_temp = wx.TextCtrl(self.second_panel, size=(80, 25), pos=(85, 50))
        self.ok_button = wx.Button(self.second_panel, label=u"ȷ���޸�", pos=(40, 80))
        self.ok_button.Bind(wx.EVT_BUTTON, self.unshow_second_panel)
        self.second_panel.Show(True)

    def unshow_second_panel(self, event):
        stunum = self.stunumvalues_temp.GetRange(0, 10)
        word = self.select_items_temp.GetSelection()
        colname = self.select_items_temp.GetItems()[word]
        colvalue = self.values_temp.GetRange(0, 30)
        if colname == u'����':
            sql = self.sqlstament.alter_info(self.table_name, colname, colvalue, u'ѧ��', stunum, 666)
        else:
            sql = self.sqlstament.alter_info(self.table_name, colname, colvalue, u'ѧ��', stunum, 333)
        self.stunumvalues_temp.Show(False)
        self.select_items_temp.Show(False)
        self.values_temp.Show(False)
        self.stunum_temp_label.Show(False)
        self.column_name_temp.Show(False)
        self.change_value.Show(False)
        self.ok_button.Show(False)
        self.sqlstament.execute_statement(sql)
        print sql


class GradesOfStudent(wx.Panel):
    def __init__(self, *args, **kwargs):
        self.table_name = u'ѧ���ɼ���Ϣ'
        super(GradesOfStudent, self).__init__(*args, **kwargs)
        title_font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)  # ��������

        self.select_item_list = [u'*', u'ѧ��', u'����', u'���ݿ�', u'���ԭ��', u'����ϵͳ', u'���ݽṹ',
                                 u'�㷨', u'���������', u'����', u'�ܳɼ�', u'ƽ���ɼ�', u'�ον�ʦ']
        self.sqlstament = MySQLTest()
        self.title_label = wx.StaticText(self, label=u"ѧ���ɼ�����", pos=(308, 10))
        self.title_label.SetFont(title_font)
        self.title_label.SetForegroundColour("#21c4c3")
        self.warning_label = wx.StaticText(self, label=u'ע:�˱�ֻ�ܹ���ѧ���Ѵ���ѧ������Ϣ.', pos=(283, 35))
        self.warning_label.SetForegroundColour('red')

        select_item_label = wx.StaticText(self, label=u"��ѯ��:", pos=(10, 10))
        value_label = wx.StaticText(self, label=u"ֵ:", pos=(96, 10))

        self.SelectButton = wx.Button(self, label=u'��ѯ', pos=(144, 30), size=(33, 25))
        self.AddButton = wx.Button(self, label=u'����һ��', pos=(680, 8), size=(60, 25))
        self.DropButton = wx.Button(self, label=u'ɾ��һ��', pos=(680, 35), size=(60, 25))
        self.UpdateButton = wx.Button(self, label=u'�޸�����', pos=(740, 8), size=(60, 25))
        self.RefreshButton = wx.Button(self, label=u'ˢ��', pos=(740, 35), size=(60, 25))
        # self.SelectButton.Bind(wx.EVT_BUTTON, self.query_info)
        # self.DropButton.Bind(wx.EVT_BUTTON, self.delete_info)
        self.AddButton.Bind(wx.EVT_BUTTON, self.add_info)
        self.RefreshButton.Bind(wx.EVT_BUTTON, self.refresh)
        # self.UpdateButton.Bind(wx.EVT_BUTTON, self.updata_info)
        self.select_items = wx.ComboBox(self, pos=(10, 30), size=(80, -1), choices=self.select_item_list,
                                        style=wx.CB_DROPDOWN)
        self.valueTextCtrl = wx.TextCtrl(self, value="", pos=(92, 30), size=(50, 25))
        self.test_grid('select * from ѧ���ɼ���Ϣ')

    def test_grid(self, sqlsta):
        import SqlUtil
        data = SqlUtil.query_data(sqlsta)
        col_label = (u'ѧ��', u'����', u'���ݿ�', u'���ԭ��', u'����ϵͳ', u'���ݽṹ',
                                 u'�㷨', u'���������', u'����', u'�ܳɼ�', u'ƽ���ɼ�', u'�ον�ʦ')
        self.testgrid = wx.grid.Grid(self, size=(800, 300), pos=(10, 60))
        row_label = []
        if len(data):
            for i in range(len(data)):
                row_label.append(i+1)
            self.testgrid.baseModel = GenericTable.GenericTable(data, row_label, col_label)
            self.testgrid.SetTable(self.testgrid.baseModel)
        else:
            wx.MessageBox('�ɼ�����������Ϣ,�������Ϣ', 'Warning!', wx.OK | wx.ICON_INFORMATION)

    def refresh(self, event):
        self.testgrid.Destroy()
        self.test_grid('select * from ѧ���ɼ���Ϣ')

    def delete_info(self, event):
        stunum = "00000000"
        entry_dlg = wx.TextEntryDialog(self, u'����һ��\"ѧ��\"��ɾ��', u'����һ��ѧ��')
        if entry_dlg.ShowModal() == wx.ID_OK:
            stunum = entry_dlg.GetValue()
        entry_dlg.Destroy()
        if stunum:
            splited_stunum = stunum.split(' ')  # ��Ϊ�û������ѧ�ſ��ܴ��ո�,�����Ȱ��ַ����ո���,�ٽ�������.(�ָ��Ϊһ������)
        # ͬ����������ʱҲ���ո���зָ�.
            joined_stunum = ''.join(splited_stunum)  # ���ѷָ����ַ���ƴ��
            stunum = joined_stunum
        sqlsta = self.sqlstament.delete_info(self.table_name, u'ѧ��', '=', stunum)
        print sqlsta
        self.sqlstament.execute_statement(sqlsta)

    def add_info(self, event):
        stu_infos = ""
        entry_dlg = wx.TextEntryDialog(self, u'����һ��ѧ����Ϣ,��ȱ����Ϣ��0����', u'����һ����Ϣ')
        if entry_dlg.ShowModal() == wx.ID_OK:
            stu_infos = entry_dlg.GetValue()
        entry_dlg.Destroy()
        if stu_infos:
            splited_stu_info = stu_infos.split(' ')
            sqlsta = self.sqlstament.insert_info_2(self.table_name, splited_stu_info)
            print sqlsta
            self.sqlstament.execute_statement(sqlsta)

    def query_info(self, event):
        self.testgrid.Destroy()
        word = self.select_items.GetSelection()
        select_item_value = self.select_items.GetItems()[word]
        value = self.valueTextCtrl.GetRange(0, 50)
        if select_item_value == u"����":
            sqlsta = self.sqlstament.select_info(self.table_name, select_item_value, '=', value, 666)
        else:
            sqlsta = self.sqlstament.select_info(self.table_name, select_item_value, '=', value, 333)
        print sqlsta
        self.test_grid(sqlsta)

    def updata_info(self, event):
        self.select_item_list2 = [u'����', u'��ͥסַ', u'�Ա�', u'����', u'�������']
        self.stunum_temp_label = wx.StaticText(self.second_panel, label=u"�޸Ķ���ѧ��:", pos=(0, 5))
        self.stunumvalues_temp = wx.TextCtrl(self.second_panel, size=(80, 25), pos=(82, 0))
        self.column_name_temp = wx.StaticText(self.second_panel, label=u"Ҫ�޸ĵ�����:", pos=(0, 30))
        self.select_items_temp = wx.ComboBox(self.second_panel, size=(80, 25), pos=(0, 50),
                                        choices=self.select_item_list2, style=wx.CB_DROPDOWN)
        self.change_value = wx.StaticText(self.second_panel, label=u'  �޸ĺ��ֵ:', pos=(82, 30))
        self.values_temp = wx.TextCtrl(self.second_panel, size=(80, 25), pos=(85, 50))
        self.ok_button = wx.Button(self.second_panel, label=u"ȷ���޸�", pos=(40, 80))
        self.ok_button.Bind(wx.EVT_BUTTON, self.unshow_second_panel)
        self.second_panel.Show(True)

    def unshow_second_panel(self, event):
        stunum = self.stunumvalues_temp.GetRange(0, 10)
        word = self.select_items_temp.GetSelection()
        colname = self.select_items_temp.GetItems()[word]
        colvalue = self.values_temp.GetRange(0, 30)
        if colname == u'����':
            sql = self.sqlstament.alter_info(self.table_name, colname, colvalue, u'ѧ��', stunum, 666)
        else:
            sql = self.sqlstament.alter_info(self.table_name, colname, colvalue, u'ѧ��', stunum, 333)
        self.stunumvalues_temp.Show(False)
        self.select_items_temp.Show(False)
        self.values_temp.Show(False)
        self.stunum_temp_label.Show(False)
        self.column_name_temp.Show(False)
        self.change_value.Show(False)
        self.ok_button.Show(False)
        self.sqlstament.execute_statement(sql)
        print sql