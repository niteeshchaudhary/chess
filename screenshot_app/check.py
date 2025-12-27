ls=["me: System Data Entity Core EntityCommandExecutionException: An error occurred while executing",
"me: the command definition: See the inner exception for details_",
"me: System Data.SqlClient SqlException: Invalid column name 'SettingDefault:",
"me: Invalid column name 'IsEncrypted' .",
"me: above error could be seen in webapi pods of env:",
"me: https IImyazuredevscs o9solutions com/Kibo2#l",
"me: its dev issue raise ADO its trying to access",
"other: Hi, Niteesh: Please upgrade the DB.",
"me: column which does not exist in db",
"other: think only the webAPI is upgraded but not the DB"]
mn=min(len(ls),3)
print("min value:",mn)
ls=ls[:mn]
print(ls[::-1])