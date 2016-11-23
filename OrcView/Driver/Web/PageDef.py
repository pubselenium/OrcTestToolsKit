# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibViewDef import def_view_page_def


class PageDefModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self)

        i_base_url = 'http://localhost:5000/PageDef'
        _interface = {
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url,
            'usr_search': '%s/usr_search' % i_base_url
        }

        self.usr_set_interface(_interface)


class PageDefControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewPageDefMag(QWidget):

    sig_selected = OrcSignal(str)
    sig_search = OrcSignal()
    sig_delete = OrcSignal()

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"用例管理"

        # Model
        self.__model = PageDefModel()
        self.__model.usr_set_definition(def_view_page_def)

        # Control
        _control = PageDefControl(def_view_page_def)

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="search", name=u"查询")
        ])

        # win_add
        self.__win_add = ViewAdd(def_view_page_def)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)

        self.__win_add.sig_submit[dict].connect(self.add)
        _wid_display.clicked[QModelIndex].connect(self.__page_detail)

    def search(self, p_cond):
        self.__model.usr_search(p_cond)

    def add(self, p_data):
        self.__model.usr_add(p_data)

    def __operate(self, p_flag):

        if "add" == p_flag:
            self.__win_add.show()
        elif "delete" == p_flag:
            self.__model.usr_delete()
            self.sig_delete.emit()
        elif "update" == p_flag:
            self.__model.usr_editable()
        elif "search" == p_flag:
            self.sig_search.emit()
        else:
            pass

    def __page_detail(self, p_index):
        _page_id = self.__model.usr_get_data(p_index.row())["id"]
        self.sig_selected[str].emit(str(_page_id))
