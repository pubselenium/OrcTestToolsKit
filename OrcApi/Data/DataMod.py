# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import func

from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import TabData
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db


class DataMod(object):
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        object.__init__(self)

    def usr_search(self, p_cond=None):
        """
        :param p_cond:
        :return:
        """
        # 判断输入参数是否为空
        cond = p_cond if p_cond else dict()

        # 查询条件 like
        _like = lambda p_flag: "%%%s%%" % cond[p_flag]

        # db session
        result = self.__session.query(TabData)

        if 'id' in cond:

            # 查询支持多 id
            if isinstance(cond["id"], list):
                result = result.filter(TabData.id.in_(cond['id']))
            else:
                result = result.filter(TabData.id == cond['id'])

        if 'src_id' in cond:
            result = result.filter(TabData.src_id.ilike(_like('src_id')))

        if 'src_type' in cond:
            result = result.filter(TabData.src_type.ilike(_like('src_type')))

        if 'data_flag' in cond:
            result = result.filter(TabData.data_flag.ilike(_like('data_flag')))

        if 'data_mode' in cond:
            result = result.filter(TabData.data_mode.ilike(_like('data_mode')))

        if 'data_type' in cond:
            result = result.filter(TabData.data_type.ilike(_like('data_type')))

        return result.all()

    def _get_root(self, p_item):
        """
        :param p_item:
        :return:
        """
        if p_item.pid is None:
            return p_item

        _res = self.__session.query(TabData).filter(TabData.id == p_item.pid).first()

        if _res.pid is None:
            return _res
        else:
            return self._get_root(_res)

    def _get_tree(self, p_item):
        """
        :param p_item:
        :return:
        """
        _tree = [p_item]
        _items = self.__session.query(TabData).filter(TabData.pid == p_item.id).all()

        for t_item in _items:
            _tree.extend(self._get_tree(t_item))

        return _tree

    def usr_add(self, p_data):
        """
        Add a new case
        :param p_data:
        :return:
        """
        _node = TabData()

        # Create id
        _node.id = gen_id("data")

        # test_env
        _node.test_env = p_data['test_env'] if 'test_env' in p_data else ""

        # src_id
        _node.src_id = p_data['src_id'] if 'src_id' in p_data else ""

        # src_type
        _node.src_type = p_data['src_type'] if 'src_type' in p_data else ""

        # data_flag
        _node.data_flag = p_data['data_flag'] if 'data_flag' in p_data else None

        # data_order
        _node.data_order = self._create_order(_node.src_id, _node.data_flag)

        # data_type
        _node.data_type = p_data['data_type'] if 'data_type' in p_data else ""

        # data_mode
        _node.data_mode = p_data['data_mode'] if 'data_mode' in p_data else ""

        # data_value
        _node.data_value = p_data['data_value'] if 'data_value' in p_data else ""

        # comment
        _node.comment = p_data['comment'] if 'comment' in p_data else ""

        # create_time, modify_time
        _node.create_time = datetime.now()
        _node.modify_time = datetime.now()

        try:
            self.__session.add(_node)
            self.__session.commit()
        except:
            raise OrcDatabaseException

        return _node

    def _create_order(self, p_id, p_flg):
        """
        Create a no, like case_no
        :return:
        """
        _order = 1
        t_item = self.__session.query(func.max(TabData.data_order))\
                     .filter(TabData.src_id == p_id)\
                     .filter(TabData.data_flag == p_flg).first()[0]

        if t_item is not None:
            _order = t_item + 1

        return _order

    def usr_update(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(TabData).filter(TabData.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_id):

        self.__session.query(TabData).filter(TabData.id == p_id).delete()
        self.__session.commit()
