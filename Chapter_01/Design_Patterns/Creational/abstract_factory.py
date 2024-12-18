from abc import ABC, abstractmethod


class AbstractReport(ABC):

    @abstractmethod
    def create_month_report(self):
        pass

    @abstractmethod
    def create_quarter_report(self):
        pass

    @abstractmethod
    def create_year_report(self):
        pass


class PdfMonthReport:
    pass


class PdfQuarterReport:
    pass


class PdfYearReport:
    pass


class PdfReport(AbstractReport):

    def create_month_report(self):
        return PdfMonthReport()

    def create_quarter_report(self):
        return PdfQuarterReport()

    def create_year_report(self):
        return PdfYearReport()


class HtmlMonthReport:
    pass


class HtmlQuarterReport:
    pass


class HtmlYearReport:
    pass


class HtmlReport(AbstractReport):

    def create_month_report(self):
        return HtmlMonthReport()

    def create_quarter_report(self):
        return HtmlQuarterReport()

    def create_year_report(self):
        return HtmlYearReport()


class CsvMonthReport:
    pass


class CsvQuarterReport:
    pass


class CsvYearReport:
    pass


class CsvReport(AbstractReport):

    def create_month_report(self):
        return CsvMonthReport()

    def create_quarter_report(self):
        return CsvQuarterReport()

    def create_year_report(self):
        return CsvYearReport()