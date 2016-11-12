# coding:gbk
# http://blog.csdn.net/chenghit/article/details/50421090  �������İ�
# http://www.cnblogs.com/dyx1024/archive/2012/07/05/2578579.html xxx
# http://blog.csdn.net/lyhdream/article/details/39702765
# http://www.cnblogs.com/hester/p/4696519.html
# http://blog.csdn.net/gzh0222/article/details/10376227
# http://blog.csdn.net/infoworld/article/details/17260627 grib
# http://tool.oschina.net/commons?type=3 ������ɫRGB��ȡ��վ
import wx
import wx.grid
import GenericTable

class RebuildFrame(wx.Frame):  # ������,���н��涼��Frame���
    def __init__(self, *args, **kwargs):
        super(RebuildFrame, self).__init__(*args, **kwargs)
        self.CreateStatusBar()

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
        self.notebook.Show(True)
        form1 = BaseInfoOfStudentPanel(self.notebook)
        form2 = ATestPanel2(self.notebook)
        form3 = ATestPanel3(self.notebook)
        self.notebook.AddPage(form1, u"������Ϣ")
        self.notebook.AddPage(form2, "test1")
        self.notebook.AddPage(form3, "test2")


class BaseInfoOfStudentPanel(wx.Panel):
    def __init__(self,  *args, **kwargs):
        super(BaseInfoOfStudentPanel, self).__init__(*args, **kwargs)
        title_font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)  # ��������

        self.login_name_label = wx.StaticText(self, label=u"ѧ��������Ϣ����", pos=(308, 10))
        select_item_label = wx.StaticText(self, label=u"��ѯ��:", pos=(10, 10))
        value_label = wx.StaticText(self, label=u"ֵ:", pos=(96, 10))
        self.login_name_label.SetFont(title_font)
        self.login_name_label.SetForegroundColour("#21c4c3")  # ����������ɫ

        select_item_list = [u'*', u'����', u'��ͥסַ', u'�Ա�', u'����', u'�������']
        self.SelectButton = wx.Button(self, label=u'��ѯ', pos=(144, 30), size=(33, 25))
        select_items = wx.ComboBox(self, pos=(10, 30), size=(80, -1), choices=select_item_list,
                                   style=wx.CB_DROPDOWN)
        self.valueTextCtrl = wx.TextCtrl(self, value="", pos=(92, 30), size=(50, 25))
        self.test_grid('select * from ѧ��������Ϣ')

    def test_grid(self, sqlsta):
        import SqlUtil
        data = SqlUtil.queryData(sqlsta)
        col_label = ("ѧ��", "����", "��ͥ��ַ", "�Ա�", "����", "�������", "A1", "B2")
        testgrid = wx.grid.Grid(self, size=(800, 300), pos=(10, 60))
        row_label = []
        for i in range(len(data)):
            row_label.append(i)
        testgrid.baseModel = GenericTable.GenericTable(data, row_label, col_label)
        testgrid.SetTable(testgrid.baseModel)


class ATestPanel2(wx.Panel):
    def __init__(self,  *args, **kwargs):
        super(ATestPanel2, self).__init__(*args, **kwargs)
        self.login_name_label = wx.StaticText(self, label=u"���.����д������-1", pos=(120, 160))


class ATestPanel3(wx.Panel):
    def __init__(self,  *args, **kwargs):
        super(ATestPanel3, self).__init__(*args, **kwargs)
        self.login_name_label = wx.StaticText(self, label=u"���.����д������-3", pos=(120, 160))

app = wx.App(False)
frame = RebuildFrame(None, title=u'ѧ�����ݿ����ϵͳ')
frame.Center()
app.MainLoop()
