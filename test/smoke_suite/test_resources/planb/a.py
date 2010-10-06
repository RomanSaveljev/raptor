
# python build extensions that don't do much

import planb.agent
import planb.target

agent = planb.agent.Connect()

bitmap = planb.target.Bitmap()
bitmap.action("echo bitmap-" + agent['PARAMS'])
agent.add_target(bitmap)

resource = planb.target.Resource()
resource.action("echo resource-" + agent['PARAMS'])
agent.add_target(resource)

target = planb.target.Target()
target.action("echo target-" + agent['PARAMS'])
agent.add_target(target)

agent.commit()
