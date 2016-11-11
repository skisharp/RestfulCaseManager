from RestfulCaseManager.util import ConfigReader


class Env():
    def __init__(self):
        pass

    @staticmethod
    def setting(module, env):
        conf = ConfigReader.read_conf(module=module)
        Env.domain = conf.get(env, "domain")
        Env.logindomain = conf.get(env, "logindomain")
        Env.passwordpostfix = conf.get(env, "passwordpostfix")
        Env.user = conf.get(env, "user")
        Env.db_oracle_username = conf.get(env, "db_oracle_username")
        Env.db_oracle_password = conf.get(env, "db_oracle_password")
        Env.db_oracle_host = conf.get(env, "db_oracle_host")
        Env.mongodb = conf.get(env, "mongodb")
        if module == 'Assess':
            Env.login_domain_answer = conf.get(env, 'login_domain_answer')



