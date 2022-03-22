# @Time    : 2022/3/10 23:14
# @Author  : ZYF
import abc

from sklearn.metrics import precision_score, recall_score, f1_score

from config import EPS

metric_with_threshold_list = []


class MetricWithThreshold(abc.ABCMeta):

    def __init_subclass__(mcs, **kwargs):
        metric_with_threshold_list.append(mcs)

    @classmethod
    @abc.abstractmethod
    def score(mcs, predict, label) -> float:
        ...


class Precision(MetricWithThreshold):
    @classmethod
    def score(mcs, predict, label) -> float:
        return precision_score(label, predict)


class Recall(MetricWithThreshold):
    @classmethod
    def score(mcs, predict, label) -> float:
        return recall_score(label, predict)


class F1(MetricWithThreshold):

    @classmethod
    def score(mcs, predict, label) -> float:
        return f1_score(label, predict)


class Fpa(MetricWithThreshold):

    @classmethod
    def score(mcs, predict, label) -> float:
        TP = 0
        TN = 0
        FN = 0
        FP = 0
        n = len(label)
        le = 0
        while le < n:
            if label[le] == 0:
                # normal
                if predict[le] == 0:
                    TN += 1
                else:
                    FP += 1
                le += 1
            else:
                # abnormal
                ri = le
                while ri < n and label[ri] == 1:
                    ri += 1
                # Anomaly
                if sum(predict[le:ri]) > 0:
                    TP += ri - le
                else:
                    FN += ri - le
                le = ri
        recall = 1.0 * TP / (TP + FN + EPS)
        precision = 1.0 * TP / (TP + FP + EPS)
        return 2.0 * recall * precision / (recall + precision + EPS)


class Fc1(MetricWithThreshold):
    @classmethod
    def score(mcs, predict, label) -> float:
        TP_t = 0
        FP_t = 0
        TP_e = 0
        FN_e = 0
        n = len(label)
        le = 0
        while le < n:
            if label[le] == 0:
                if predict[le] == 1:
                    FP_t += 1
                le += 1
            else:
                ri = le
                while ri < n and label[ri] == 1:
                    ri += 1
                if sum(predict[le:ri]) > 0:
                    TP_t += sum(predict[le:ri])
                    TP_e += 1
                else:
                    FN_e += 1
                le = ri
        recall = 1.0 * TP_e / (TP_e + FN_e + EPS)
        precision = 1.0 * TP_t / (TP_t + FP_t + EPS)
        return 2.0 * recall * precision / (recall + precision + EPS)


if __name__ == '__main__':
    x = [0, 1, 0, 1, 1, 0]
    y = [0, 1, 1, 1, 0, 1]
    print(Precision.score(x, y))
    print(metric_with_threshold_list)
    for metric in metric_with_threshold_list:
        print(metric.__name__, metric.score(x, y))
