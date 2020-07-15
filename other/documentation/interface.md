# The Firefly Chi Plugin Interface
Official plugins are located in the plugins directory.



### Writing a plugin
Plugins are necessary to make the system actually do something. Moving 
implementation details to plugins allows users to hot-swap components
through configs.

#### Hooks
Hooks are what allow plugins to run at certain times. 
