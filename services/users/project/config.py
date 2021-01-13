class BaseConfig:
    """Base configuration"""
    TESTING = False
    JSONIFY_PRETTYPRINT_REGULAR = False

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    pass

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True

class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass
