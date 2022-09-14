
/* 
********************************************************************************************************
Вывод списка АРМ с МНИ для ЦИТСиЗИ
********************************************************************************************************
*/

COPY (
	
SELECT 
	public.computers_isod.comp_reg_num																AS "№ п/п",
	public.property.prop_factory_num																AS "Заводской номер АРМ"
FROM 
	public.computers_isod
	-- Присоеденяем таблицу "computers_isod"
	LEFT OUTER JOIN public.property 		ON public.computers_isod.fk_prop = public.property.prop_id
	
GROUP BY
)
TO 'C:\Apache24\htdocs\1.csv'
--WITH CSV;
DELIMITER E'\t'
NULL AS ''
CSV;

/* 
********************************************************************************************************
Вывод списка АРМ с МНИ для ЦИТСиЗИ (старый вариант для образца)
********************************************************************************************************
*/

COPY (
SELECT 
	public.computers_isod.comp_reg_num																AS "№ п/п",
	public.computers_isod.comp_factory_num															AS "Заводской номер АРМ",
	array_to_string(array_agg(public.disk_storage_isod.disk_model	|| '/' || 	
							  public.disk_storage_isod.disk_size), E';\n')	AS "Модель МНИ/ объем",
	array_to_string(array_agg(public.disk_storage_isod.disk_factory_num), E';\n')			AS "Заводской номер МНИ",
	array_to_string(array_agg(public.disk_storage_isod.disk_reg_num), E';\n')			AS "Регистрационный номер МНИ",
	public.computers_isod.comp_mac_address 															AS "МАС адрес сетевой карты",
	public.computers_isod.comp_ip_address 															AS "IP-адрес",
	public.computers_isod.comp_virt_ip_address 														AS "Виртуальный IP-адрес",
	public.computers_isod.comp_id_dst_file 															AS "ID  DST", 
	public.computers_isod.comp_title_dst_file 														AS "Имя DST", 
	'г. Брянск, пр-т Ленина д. 18, кабинет № ' || public.cabinets.cab_num				AS "Адрес дислокации АРМ",
	public.employees.emp_surname			|| ' ' ||
		public.employees.emp_name			|| ' ' ||
		public.employees.emp_middle_name 	|| ', '	||
		public.positions.pos_title																	AS "Ф.И.О., должность пользователя", 
	public.computers_isod.comp_attestation_status 							AS "Состояние аттестации АРМ"
FROM 
	public.computers_isod
	-- Присоеденяем таблицу "disk_storage_isod"
	LEFT OUTER JOIN public.disk_storage_isod 	ON public.computers_isod.comp_id = public.disk_storage_isod.fk_install_in_comp
	-- Присоеденяем таблицу "cabinets"
	LEFT OUTER JOIN public.cabinets 		ON public.computers_isod.fk_cabinet_location = public.cabinets.cab_id
	-- Присоеденяем таблицу "employees"
	LEFT OUTER JOIN public.employees 		ON public.computers_isod.fk_comp_owner = public.employees.emp_id
	-- Присоеденяем таблицу "positions"
	LEFT OUTER JOIN public.positions 		ON public.employees.fk_position = public.positions.pos_id
GROUP BY
	public.computers_isod.comp_id,	
	public.cabinets.cab_id,
	public.employees.emp_id,
	public.positions.pos_id
)
TO 'C:\Apache24\htdocs\1.csv'
--WITH CSV;
DELIMITER E'\t'
NULL AS ''
CSV;

/*********************************************************************************************************
Выбор списка подразделений, отделов и отделений
*********************************************************************************************************/
SELECT
	div_title 		AS "Подразделение",
	dep_first_title		AS "Отдел",
	dep_second_title	AS "Отделение"
FROM public.divisions
	LEFT OUTER JOIN public.departments_first 	ON public.divisions.div_id = public.departments_first.fk_div
	LEFT OUTER JOIN public.departments_second 	ON public.departments_first.dep_first_id = public.departments_second.fk_dep_first


/*********************************************************************************************************
Выбор списка сотрудников c должностью и статусом
*********************************************************************************************************/
SELECT 
	public.employees.emp_id                     AS 	"Номер",
	public.employees.emp_surname                AS 	"Фамилия",
	public.employees.emp_name                   AS 	"Имя",
	public.employees.emp_middle_name            AS 	"Отчество",
	public.employees.emp_birthday               AS 	"Дата рождения",
	public.positions.pos_title                  AS 	"Должность",
	public.departments_second.dep_second_title  AS 	"Отделение",
	public.departments_first.dep_first_title    AS 	"Отдел",
	public.types_work.tw_title                  AS 	"Вид службы",
	public.employees_status.emp_status          AS 	"Статус сотрудника"
FROM
	-- Выбираем таблицу с сотрудниками
	public.employees 
	-- Присоеденяем таблицу "positions" (должности)
	LEFT OUTER JOIN public.positions            ON public.employees.fk_position = public.positions.pos_id
	-- Присоеденяем таблицу "departments_second" (отделения)
	LEFT OUTER JOIN public.departments_second   ON public.positions.fk_dep_second = public.departments_second.dep_second_id
	-- Присоеденяем таблицу "departments_first" (отделы)
	LEFT OUTER JOIN public.departments_first    ON public.positions.fk_dep_first = public.departments_first.dep_first_id
	-- Присоеденяем таблицу "employees_status" (статусы сотрудников)
	LEFT OUTER JOIN public.employees_status     ON public.employees_status.emp_st_id = public.employees.fk_position
	-- Присоеденяем таблицу "types_work" (вид службы)
	LEFT OUTER JOIN public.types_work           ON public.positions.fk_types_work = public.types_work.tw_id
