# python FLM generator for TOOLS2 EXE

import planb.agent
import planb.tools2

agent = planb.agent.Connect()

target = planb.tools2.Exe(agent['TARGET'], agent)

# the Exe object could get all its values from the agent, but show here
# how an MMP could be replaced using these objects.

target.add_user_includes(agent['USERINCLUDE'].split())
target.add_system_includes(agent['SYSTEMINCLUDE'].split())
target.add_source_files(agent['SOURCE'].split())
target.add_static_libraries(agent['STATICLIBRARY'].split())
target.finalise()

agent.commit()