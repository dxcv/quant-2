from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from .ABuFactorBuyBase import AbuFactorBuyBase, AbuFactorBuyXD, BuyCallMixin, BuyPutMixin

class XcFactorBuyRsi(AbuFactorBuyBase, BuyCallMixin):
    """示例正向突破买入择时类，混入BuyCallMixin，即向上突破触发买入event"""

    def _init_self(self, **kwargs):
        """kwargs中必须包含: 突破参数xd 比如20，30，40天...突破"""
        self.rsi = kwargs['rsi']
        # 在输出生成的orders_pd中显示的名字
        self.factor_name = '{}:{}'.format(self.__class__.__name__, self.rsi)

    def fit_day(self, today):
        """
        
        :param today: 当前驱动的交易日金融时间序列数据
        :return:
        """
        # 低于20，并再次超过20的时候，买入
        if today['rsi15']<=20:

            self.status_one = True
       
        if self.status_one == True and today['rsi15']>30:
            self.status_one = False
            return self.buy_today()

        return None