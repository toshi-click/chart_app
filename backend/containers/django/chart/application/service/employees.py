import logging

from django.db import transaction, connection
from django.utils import timezone
from django.utils.timezone import localtime

from chart.application.enums.department_type import DepartmentType
from chart.application.enums.gender_type import GenderType
from chart.application.service.app_logic_base import AppLogicBaseService
from chart.models import Employees, Departments

"""
employeesテーブルを操作するクラスです。
"""
class EmployeesService(AppLogicBaseService):
    def __init__(self):
        super().__init__()

    @staticmethod
    @transaction.atomic()
    def create_employees():
        """
        Employeesを作成する
        """
        service = EmployeesService()

        for emp_no in range(1, 11):
            if Employees.objects.filter(emp_no=emp_no, delete_flag=0).count() == 0:
                if emp_no <= 5:
                    department_no = DepartmentType.SALES.value
                else:
                    department_no = DepartmentType.MARKETING.value
                select_model = Departments.objects.filter(department_no=department_no).values("id").first()
                # データを登録する
                service._regist_employees(select_model['id'], emp_no)

    @staticmethod
    @transaction.atomic()
    def create_departments():
        """
        Departmentsを作成する
        """
        service = EmployeesService()

        # データをすべて削除する
        # ForeignKeyが指定されているためdeleteコマンドを実行する
        Departments.objects.all().delete()

        for department_type in DepartmentType:
            department_no = department_type.value
            if Departments.objects.filter(department_no=department_no, delete_flag=0).count() == 0:
                # データを登録する
                service._regist_departments(department_no, department_type.en_name)

    @staticmethod
    @transaction.atomic()
    def update_employees():
        """
        Employeesを更新する
        """
        service = EmployeesService()

        # filterによる絞込を行う
        # gt:...より大きい(>),lt:...より小さい(<)になる
        for employees_item in Employees.objects.filter(emp_no__gt=1, emp_no__lt=3, delete_flag=0):
            employees_id = employees_item.id
            select_model = Departments.objects.filter(department_no=DepartmentType.PRODUCTION.value).values(
                "id").first()
            department_id = select_model['id']
            department_date_from = 20190903
            # データを更新する
            service._update_employees_department(employees_id, department_id, department_date_from)

        # filterによる絞込を行う
        # gte:...以上(>=),lte:...以下(<=)になる
        for employees_item in Employees.objects.filter(emp_no__gte=7, emp_no__lte=9, delete_flag=0):
            employees_id = employees_item.id
            select_model = Departments.objects.filter(department_no=DepartmentType.SALES.value).values("id").first()
            department_id = select_model['id']
            department_date_from = 20190905
            # データを更新する
            service._update_employees_department(employees_id, department_id, department_date_from)

    @staticmethod
    def select_employees():
        """
        Employeesを検索する
        """
        # テーブル名__項目名で指定するとINNER JOINになる
        # Queryは参照先のテーブルを参照する度に発行されます
        for employees_item in Employees.objects.filter(department__department_no=DepartmentType.SALES.value,
                                                       delete_flag=0):
            logging.debug("reference:emp_no={}".format(employees_item.emp_no))
            logging.debug("reference:department_no={}".format(employees_item.department.department_no))
            logging.debug("reference:department_name={}".format(employees_item.department.department_name))
            logging.debug("reference:first_name={}".format(employees_item.first_name))
            logging.debug("reference:last_name={}".format(employees_item.last_name))

        # select_relatedを使用した参照先情報を取得してキャッシュします
        # Queryは1回のみ発行されます
        for employees_item in Employees.objects.filter(emp_no__gte=7, delete_flag=0).select_related("department"):
            logging.debug("select_related:emp_no={}".format(employees_item.emp_no))
            logging.debug("select_related:first_name={}".format(employees_item.first_name))
            logging.debug("select_related:last_name={}".format(employees_item.last_name))
            logging.debug("select_related:department_no={}".format(employees_item.department.department_no))
            logging.debug("select_related:department_name={}".format(employees_item.department.department_name))

        # prefetch_relatedを使用した参照先情報を取得してキャッシュします
        # Queryは2回発行されてForeignKeyで結合します
        for employees_item in Employees.objects.filter(emp_no__gte=7, delete_flag=0).prefetch_related(
                "department__employees_set"):
            logging.debug("prefetch_related:emp_no={}".format(employees_item.emp_no))
            logging.debug("prefetch_related:first_name={}".format(employees_item.first_name))
            logging.debug("prefetch_related:last_name={}".format(employees_item.last_name))
            logging.debug("prefetch_related:department_no={}".format(employees_item.department.department_no))
            logging.debug("prefetch_related:department_name={}".format(employees_item.department.department_name))

    @staticmethod
    @transaction.atomic()
    def truncate_employees():
        """
        トランケートを行う
        """
        cursor = connection.cursor()
        cursor.execute('TRUNCATE TABLE {0}'.format(Employees._meta.db_table))

    def _regist_employees(self, department_id, emp_no):
        """
        employeesを登録する
        """
        self.regist_model = Employees()
        self.regist_model.emp_no = emp_no
        self.regist_model.department_id = department_id
        self.regist_model.first_name = "first_name_" + str(emp_no).zfill(3)
        self.regist_model.last_name = "last_name_" + str(emp_no).zfill(3)
        self.regist_model.gender = GenderType.MAN.value
        self.regist_model.department_date_from = "20190902"
        self.regist_model.delete_flag = 0
        self.regist_model.regist_dt = localtime(timezone.now())
        self.regist_model.update_dt = localtime(timezone.now())
        self.regist_model.save()
        return self.regist_model.id

    def _regist_departments(self, department_no, department_name):
        """
        departmentsを登録する
        """
        self.regist_model = Departments()
        self.regist_model.department_no = department_no
        self.regist_model.department_name = department_name
        self.regist_model.delete_flag = 0
        self.regist_model.regist_dt = localtime(timezone.now())
        self.regist_model.update_dt = localtime(timezone.now())
        self.regist_model.save()

    def _update_employees_department(self, employees_id, department_id, department_date_from):
        """
        配属情報を更新する
        """
        self.update_model = Employees()
        self.update_model.pk = employees_id
        self.update_model.department_id = department_id
        self.update_model.department_date_from = department_date_from
        self.update_model.update_dt = localtime(timezone.now())
        self.update_model.save(update_fields=['department_id', 'department_date_from', 'update_dt'])
