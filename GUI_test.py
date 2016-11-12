# coding:gbk
# http://blog.csdn.net/chenghit/article/details/50421090  �������İ�
# http://www.cnblogs.com/dyx1024/archive/2012/07/05/2578579.html xxx
# http://blog.csdn.net/lyhdream/article/details/39702765
# http://www.cnblogs.com/hester/p/4696519.html
# http://blog.csdn.net/gzh0222/article/details/10376227
# http://blog.csdn.net/infoworld/article/details/17260627 grib
# http://tool.oschina.net/commons?type=3 ������ɫRGB��ȡ��վ
# http://www.yiibai.com/wxpython/wx_dialog_class.html
# http://www.cnblogs.com/ankier/archive/2012/10/14/2723364.html
import wx
import wx.grid
import GenericTable
from SQL_test import MySQLTest


class RebuildFrame(wx.Frame):  # ������,���н��涼��Frame���
    def __init__(self, *args, **kwargs):
        super(RebuildFrame, self).__init__(*args, **kwargs)
        self.CreateStatusBar()
        self.show_elements = False

        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program.")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "&Save", " Save information.")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "&Exit", " Terminate the program.")

        menu_bar = wx.MenuBar()
        menu_bar.Append(filemenu, "&File")
        self.SetMenuBar(menu_bar)

        self.login_panel = wx.Panel(self, 1)

        self.notebook = wx.Notebook(self.login_panel, size=(830, 400))
        self.notebook.Show(False)

        self.login_name_Label = wx.StaticText(self.login_panel, label=u"ѧ���ɼ�����ϵͳ")
        self.confirm_button = wx.Button(self.login_panel, label=u"��¼")
        self.username_label = wx.StaticText(self.login_panel, label=u"�û���")
        self.password = wx.StaticText(self.login_panel, label=u"����")
        self.nameTextCtrl = wx.TextCtrl(self.login_panel, value="")
        self.passwordTextCtrl = wx.TextCtrl(self.login_panel, value=u"", style=wx.TE_PASSWORD)
        self.Bind(wx.EVT_BUTTON, self.confisrm_button, self.confirm_button)

        self.do_layout()
        self.SetClientSize((830, 400))  # (��, ��)
        self.Show()

    def do_layout(self):
        for control, x, y, width, height in \
                [(self.login_name_Label, 360, 90, -1, -1),
                 (self.username_label, 290, 150, -1, -1),
                 (self.nameTextCtrl, 330, 148, 150, 25),
                 (self.password, 295, 183, -1, -1),
                 (self.passwordTextCtrl, 330, 178, 150, 25),
                 (self.confirm_button, 350, 210, -1, -1)
                 ]:
            control.SetDimensions(x=x, y=y, width=width, height=height)

    def confisrm_button(self, event):
        self.show_elements = False
        self.show_element(self.show_elements)
        self.notebook.Show(True)
        form1 = BaseInfoOfStudentPanel(self.notebook)
        form2 = GradesOfStudent(self.notebook)
        form3 = ATestPanel3(self.notebook)
        self.notebook.AddPage(form1, u"������Ϣ")
        self.notebook.AddPage(form2, "test1")
        self.notebook.AddPage(form3, "test2")

    def show_element(self, show_elements):
        self.login_name_Label.Show(show_elements)
        self.confirm_button.Show(show_elements)
        self.username_label.Show(show_elements)
        self.password.Show(show_elements)
        self.nameTextCtrl.Show(show_elements)
        self.passwordTextCtrl.Show(show_elements)


class BaseInfoOfStudentPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        self.sqlstament = MySQLTest()
        self.table_name = u'ѧ��������Ϣ'
        super(BaseInfoOfStudentPanel, self).__init__(*args, **kwargs)
        title_font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)  # ��������

        self.title_label = wx.StaticText(self, label=u"ѧ��������Ϣ����", pos=(308, 10))
        select_item_label = wx.StaticText(self, label=u"��ѯ��:", pos=(10, 10))
        value_label = wx.StaticText(self, label=u"ֵ:", pos=(96, 10))
        self.title_label.SetFont(title_font)
        self.title_label.SetForegroundColour("#21c4c3")  # ����������ɫ

        self.SelectButton = wx.Button(self, label=u'��ѯ', pos=(144, 30), size=(33, 25))
        self.AddButton = wx.Button(self, label=u'���һ��', pos=(700, 8), size=(60, 25))
        self.DropButton = wx.Button(self, label=u'ɾ��һ��', pos=(700, 35), size=(60, 25))
        self.UpdateButton = wx.Button(self, label=u'�޸�\n����', pos=(764, 25), size=(35, 45))
        self.RefreshButton = wx.Button(self, label=u'ˢ��', pos=(700, 62), size=(60, 25))
        self.SelectButton.Bind(wx.EVT_BUTTON, self.query_info)
        self.DropButton.Bind(wx.EVT_BUTTON, self.delete_info)
        self.AddButton.Bind(wx.EVT_BUTTON, self.add_info)
        self.RefreshButton.Bind(wx.EVT_BUTTON, self.refresh)

        select_item_list = [u'*', u'����', u'��ͥסַ', u'�Ա�', u'����', u'�������']
        self.select_items = wx.ComboBox(self, pos=(10, 30), size=(80, -1), choices=select_item_list,
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
        # ͬ���������ʱҲ���ո���зָ�.
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
        word = self.select_items.GetSelection()
        select_item_value = self.select_items.GetItems()[word]
        value = self.valueTextCtrl.GetRange(0, 50)
        # print select_item_value + "   " + value

    def updata_info(self, event):
        content = ""
        entry_dlg = wx.TextEntryDialog(self, u'������Ҫ�޸ĵ�������ֵ,������ѧ��', u'����һ����Ϣ')
        if entry_dlg.ShowModal() == wx.ID_OK:
            content = entry_dlg.GetValue()
        entry_dlg.Destroy()
        if content:
            splited_content = content.split(" ")
        return content


class GradesOfStudent(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(GradesOfStudent, self).__init__(*args, **kwargs)
        title_font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)  # ��������

        self.title_label = wx.StaticText(self, label=u"ѧ���ɼ�����", pos=(308, 10))
        self.title_label.SetFont(title_font)
        self.title_label.SetForegroundColour("#21c4c3")
        self.warning_label = wx.StaticText(self, label=u'ע:�˱�ֻ�ܹ���ѧ���Ѵ���ѧ������Ϣ.', pos=(283, 35))
        self.warning_label.SetForegroundColour('red')


class ATestPanel3(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(ATestPanel3, self).__init__(*args, **kwargs)
        self.login_name_label = wx.StaticText(self, label=u"���.����д������-3", pos=(120, 160))


app = wx.App(False)
frame = RebuildFrame(None, title=u'ѧ�����ݿ����ϵͳ')
frame.Center()
app.MainLoop()
