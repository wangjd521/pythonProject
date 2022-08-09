import pandas as pd

data = pd.read_excel('switch.xlsx')

with open('nso-inventroy.cfg', 'w') as f:

    for i in data.index:
        f.write('devices device ' + data['Device Name'][i] + '\n')
        f.write('address ' + data['Management IP'][i] + '\n')
        f.write('ssh host-key-verification none \n')
        f.write('authgroup genpact-access-switch \n')
        f.write('device-type cli ned-id cisco-ios-cli-6.69 \n')
        f.write('device-type cli protocol ssh \n')
        f.write('state admin-state unlocked \n')
        f.write('! \n')
