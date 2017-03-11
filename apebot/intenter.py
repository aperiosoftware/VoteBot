from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine


class IntentCaller:
    """
    This class keeps a mapping between intents and methods.
    """
    def __init__(self, engine=None):
        if not engine:
            engine = IntentDeterminationEngine()

        self.engine = engine
        self.intentmapper = {}

    def get_function(self, message):
        """
        Query the Intent Engine to find the callable associated with the
        message.
        """
        for intent in self.engine.determine_intent(message):
            if intent.get('confidence') > 0:
                func = self.intentmapper.get(intent.get('intent_type'), None)
                if func:
                    return func
                else:
                    raise ValueError("No function associated with intent {}".format(intent.get('intent_type')))

    def register_entity(self, name, iterable):
        """
        Given a name and a list of things register them as an entity with the
        engine.
        """
        for item in iterable:
            self.engine.register_entity(item, name)
        return lambda func: func

    def register_intent(self, intent):
        """
        Store a function as an intent
        """
        self.engine.register_intent_parser(intent)
        def decorator(func):
            self.intentmapper[intent.name] = func
            return func
        return decorator

    def keyword_trigger(self, keyword, name=None):
        """
        Register a single keyword as a command.
        """
        if not name:
            name = "trigger{}".format(keyword)
        self.register_entity(name, [keyword])
        intent = IntentBuilder("{}Intent".format(keyword)).require(name).build()
        return self.register_intent(intent)
