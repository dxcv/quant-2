from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from .ABuFactorSellBase import AbuFactorSellBase, ESupportDirection

g_stop_n = 1.5

class XcFactorSellNormal(AbuFactorSellBase):
    """涨跌百分之g_stop_n卖出"""

    def _init_self(self, **kwargs):
        """kwargs中可选参数pre_atr_n: 单日最大跌幅止损的atr倍数"""

        self.stop_n = g_stop_n
        if 'stop_loss_n' in kwargs:
            # 设置止损的atr倍数
            self.stop_loss_n = kwargs['stop_loss_n']
            # 在输出生成的orders_pd中及可视化等等显示的名字
            self.sell_type_extra_loss = '{}:stop_loss={}'.format(self.__class__.__name__, self.stop_loss_n)

        if 'stop_win_n' in kwargs:
            # 设置止盈的atr倍数
            self.stop_win_n = kwargs['stop_win_n']
            # 在输出生成的orders_pd中及可视化等等显示的名字
            self.sell_type_extra_win = '{}:stop_win={}'.format(self.__class__.__name__, self.stop_win_n)

    def support_direction(self):
        """单日最大跌幅n倍atr(止损)因子支持两个方向"""
        return [ESupportDirection.DIRECTION_CAll.value, ESupportDirection.DIRECTION_PUT.value]

    def fit_day(self, today, orders):
        """
        止损event：今天相比昨天的收益 * 买入时的期望方向 > today.atr21 * pre_atr_n
        :param today: 当前驱动的交易日金融时间序列数据
        :param orders: 买入择时策略中生成的订单序列
        :return:
        """

        for order in orders:
            profit = (today.close - order.buy_price) * order.expect_direction
            if hasattr(self, 'stop_n') and profit > 0 and profit > self.stop_n * order.buy_price / 100:
                # 满足止盈条件卖出股票, 即收益(profit) > n倍atr
                self.sell_type_extra = self.sell_type_extra_win
                # 由于使用了当天的close价格，所以明天才能卖出
                #self.sell_tomorrow(order)
                self.sell_today(order)
            if hasattr(self, 'stop_n') and profit < 0 and abs(profit) > self.stop_n * order.buy_price / 100:
                # 满足止盈条件卖出股票, 即收益(profit) > n倍atr
                self.sell_type_extra = self.sell_type_extra_loss
                # 由于使用了当天的close价格，所以明天才能卖出
                self.sell_today(order)