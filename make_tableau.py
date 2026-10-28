import os
import zipfile

# Tableau .twb is just XML under the hood.
# Writing the XML directly to assemble the 6 sheets + dashboard layout,
# then zipping it with the CSV so it opens on any computer as a .twbx.

csv_name = 'cleaned_indian_startup_funding.csv'

twb_content = f"""<?xml version='1.0' encoding='utf-8' ?>
<workbook source-build='2024.1.0' source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <document-format-change-manifest>
    <AccessibleZoneTabOrder />
    <AnimationOnByDefault />
    <AutoCreateAndUpdateDOPT />
    <MapboxVectorStylesAndLayers />
    <MarkAnimation />
    <SheetIdentifierTracking />
    <WindowsPersistSimpleIdentifiers />
  </document-format-change-manifest>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>
  <datasources>
    <datasource caption='cleaned_indian_startup_funding' inline='true' name='federated.startup_funding' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='cleaned_indian_startup_funding' name='textscan.startup_conn'>
            <connection class='textscan' directory='.' filename='{csv_name}' password='' server='' />
          </named-connection>
        </named-connections>
        <relation connection='textscan.startup_conn' name='{csv_name}' table='[{csv_name}]' type='table'>
          <columns character-set='UTF-8' header='yes' locale='en_US' separator=','>
            <column datatype='date' name='Date' ordinal='0' />
            <column datatype='string' name='Startup Name' ordinal='1' />
            <column datatype='string' name='Industry Vertical' ordinal='2' />
            <column datatype='string' name='City/Location' ordinal='3' />
            <column datatype='string' name='Investors' ordinal='4' />
            <column datatype='string' name='Investment Type' ordinal='5' />
            <column datatype='real' name='Amount in USD' ordinal='6' />
          </columns>
        </relation>
        <metadata-records>
          <metadata-record class='column'>
            <remote-name>Date</remote-name>
            <remote-type>133</remote-type>
            <local-name>[Date]</local-name>
            <parent-name>[{csv_name}]</parent-name>
            <type>date</type>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Startup Name</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Startup Name]</local-name>
            <parent-name>[{csv_name}]</parent-name>
            <type>string</type>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Industry Vertical</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Industry Vertical]</local-name>
            <parent-name>[{csv_name}]</parent-name>
            <type>string</type>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>City/Location</remote-name>
            <remote-type>129</remote-type>
            <local-name>[City/Location]</local-name>
            <parent-name>[{csv_name}]</parent-name>
            <type>string</type>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Investors</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Investors]</local-name>
            <parent-name>[{csv_name}]</parent-name>
            <type>string</type>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Investment Type</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Investment Type]</local-name>
            <parent-name>[{csv_name}]</parent-name>
            <type>string</type>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Amount in USD</remote-name>
            <remote-type>5</remote-type>
            <local-name>[Amount in USD]</local-name>
            <parent-name>[{csv_name}]</parent-name>
            <type>real</type>
            <contains-null>true</contains-null>
          </metadata-record>
        </metadata-records>
      </connection>
      <aliases enabled='yes' />
      <column datatype='real' default-format='C1033,&quot;$&quot;#,##0;(&quot;$&quot;#,##0)' name='[Amount in USD]' role='measure' type='quantitative' />
      <column datatype='string' name='[City/Location]' role='dimension' semantic-role='[City].[Name]' type='nominal' />
      <column datatype='string' name='[Industry Vertical]' role='dimension' type='nominal' />
      <column datatype='string' name='[Investment Type]' role='dimension' type='nominal' />
      <column datatype='string' name='[Startup Name]' role='dimension' type='nominal' />
      <column datatype='date' name='[Date]' role='dimension' type='ordinal' />
      <column-instance column='[Amount in USD]' derivation='Sum' name='[sum:Amount in USD:qk]' pivot='key' type='quantitative' />
      <column-instance column='[Amount in USD]' derivation='Avg' name='[avg:Amount in USD:qk]' pivot='key' type='quantitative' />
      <column-instance column='[Amount in USD]' derivation='Count' name='[cnt:Deals:qk]' pivot='key' type='quantitative' />
      <layout dim-ordering='alphabetic' dim-percentage='0.5' measure-ordering='alphabetic' measure-percentage='0.5' show-structure='true' />
      <semantic-values>
        <semantic-value key='[Country].[Name]' value='&quot;India&quot;' />
      </semantic-values>
    </datasource>
  </datasources>

  <worksheets>
    <worksheet name='KPI Overview'>
      <table>
        <view>
          <datasources>
            <datasource caption='cleaned_indian_startup_funding' name='federated.startup_funding' />
          </datasources>
          <datasource-dependencies datasource='federated.startup_funding'>
            <column datatype='real' default-format='C1033,&quot;$&quot;#,##0;(&quot;$&quot;#,##0)' name='[Amount in USD]' role='measure' type='quantitative' />
            <column-instance column='[Amount in USD]' derivation='Sum' name='[sum:Amount in USD:qk]' pivot='key' type='quantitative' />
            <column-instance column='[Amount in USD]' derivation='Count' name='[cnt:Amount in USD:qk]' pivot='key' type='quantitative' />
            <column-instance column='[Amount in USD]' derivation='Avg' name='[avg:Amount in USD:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='mark'>
            <encoding attr='color' value='#B3541E' />
          </style-rule>
          <style-rule element='gridline'>
            <format attr='stroke-size' value='0' />
            <format attr='line-style' value='none' />
          </style-rule>
          <style-rule element='zeroline'>
            <format attr='stroke-size' value='0' />
            <format attr='line-style' value='none' />
          </style-rule>
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Text' />
            <encodings>
              <text column='[federated.startup_funding].[sum:Amount in USD:qk]' />
            </encodings>
          </pane>
        </panes>
        <rows />
        <cols />
      </table>
    </worksheet>

    <worksheet name='Funding Trend'>
      <layout-options>
        <title>
          <formatted-text>
            <run bold='true' fontcolor='#111827' fontname='Georgia' fontsize='14'>Funding peaked in 2021 — sharp correction since</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='cleaned_indian_startup_funding' name='federated.startup_funding' />
          </datasources>
          <datasource-dependencies datasource='federated.startup_funding'>
            <column datatype='date' name='[Date]' role='dimension' type='ordinal' />
            <column datatype='real' default-format='C1033,&quot;$&quot;#,##0;(&quot;$&quot;#,##0)' name='[Amount in USD]' role='measure' type='quantitative' />
            <column-instance column='[Date]' derivation='Year' name='[yr:Date:ok]' pivot='key' type='ordinal' />
            <column-instance column='[Amount in USD]' derivation='Sum' name='[sum:Amount in USD:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='axis'>
            <encoding attr='space' class='0' field='[federated.startup_funding].[sum:Amount in USD:qk]' field-type='quantitative' fold='true' scope='rows' type='space' />
          </style-rule>
          <style-rule element='mark'>
            <encoding attr='color' value='#B3541E' />
          </style-rule>
          <style-rule element='gridline'>
            <format attr='stroke-size' value='0' />
            <format attr='line-style' value='none' />
          </style-rule>
          <style-rule element='zeroline'>
            <format attr='stroke-size' value='0' />
            <format attr='line-style' value='none' />
          </style-rule>
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Area' />
            <encodings>
              <color value='#B3541E' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.startup_funding].[sum:Amount in USD:qk]</rows>
        <cols>[federated.startup_funding].[yr:Date:ok]</cols>
      </table>
    </worksheet>

    <worksheet name='Sector Share'>
      <layout-options>
        <title>
          <formatted-text>
            <run bold='true' fontcolor='#111827' fontname='Georgia' fontsize='14'>Top 3 sectors absorb nearly half of all capital</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='cleaned_indian_startup_funding' name='federated.startup_funding' />
          </datasources>
          <datasource-dependencies datasource='federated.startup_funding'>
            <column datatype='string' name='[Industry Vertical]' role='dimension' type='nominal' />
            <column datatype='real' default-format='C1033,&quot;$&quot;#,##0;(&quot;$&quot;#,##0)' name='[Amount in USD]' role='measure' type='quantitative' />
            <column-instance column='[Industry Vertical]' derivation='None' name='[none:Industry Vertical:nk]' pivot='key' type='nominal' />
            <column-instance column='[Amount in USD]' derivation='Sum' name='[sum:Amount in USD:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='mark'>
            <encoding attr='color' value='#B3541E' />
          </style-rule>
          <style-rule element='gridline'>
            <format attr='stroke-size' value='0' />
            <format attr='line-style' value='none' />
          </style-rule>
          <style-rule element='zeroline'>
            <format attr='stroke-size' value='0' />
            <format attr='line-style' value='none' />
          </style-rule>
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Bar' />
            <encodings>
              <color value='#B3541E' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.startup_funding].[none:Industry Vertical:nk]</rows>
        <cols>[federated.startup_funding].[sum:Amount in USD:qk]</cols>
      </table>
    </worksheet>

    <worksheet name='City Map'>
      <layout-options>
        <title>
          <formatted-text>
            <run bold='true' fontcolor='#111827' fontname='Georgia' fontsize='14'>Bangalore, Mumbai and Delhi-NCR dominate deal flow</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='cleaned_indian_startup_funding' name='federated.startup_funding' />
          </datasources>
          <datasource-dependencies datasource='federated.startup_funding'>
            <column datatype='string' name='[City/Location]' role='dimension' semantic-role='[City].[Name]' type='nominal' />
            <column datatype='real' default-format='C1033,&quot;$&quot;#,##0;(&quot;$&quot;#,##0)' name='[Amount in USD]' role='measure' type='quantitative' />
            <column-instance column='[City/Location]' derivation='None' name='[none:City/Location:nk]' pivot='key' type='nominal' />
            <column-instance column='[Amount in USD]' derivation='Sum' name='[sum:Amount in USD:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Circle' />
            <encodings>
              <size column='[federated.startup_funding].[sum:Amount in USD:qk]' />
              <color value='#B3541E' />
              <lod column='[federated.startup_funding].[none:City/Location:nk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.startup_funding].[Latitude]</rows>
        <cols>[federated.startup_funding].[Longitude]</cols>
      </table>
    </worksheet>

    <worksheet name='Stage Mix'>
      <layout-options>
        <title>
          <formatted-text>
            <run bold='true' fontcolor='#111827' fontname='Georgia' fontsize='14'>Early-stage share fell 13 points (33% to 20%)</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='cleaned_indian_startup_funding' name='federated.startup_funding' />
          </datasources>
          <datasource-dependencies datasource='federated.startup_funding'>
            <column datatype='date' name='[Date]' role='dimension' type='ordinal' />
            <column datatype='string' name='[Investment Type]' role='dimension' type='nominal' />
            <column datatype='real' name='[Amount in USD]' role='measure' type='quantitative' />
            <column-instance column='[Date]' derivation='Year' name='[yr:Date:ok]' pivot='key' type='ordinal' />
            <column-instance column='[Investment Type]' derivation='None' name='[none:Investment Type:nk]' pivot='key' type='nominal' />
            <column-instance column='[Amount in USD]' derivation='Count' name='[cnt:Deals:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='gridline'>
            <format attr='stroke-size' value='0' />
            <format attr='line-style' value='none' />
          </style-rule>
          <style-rule element='zeroline'>
            <format attr='stroke-size' value='0' />
            <format attr='line-style' value='none' />
          </style-rule>
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Bar' />
            <encodings>
              <color column='[federated.startup_funding].[none:Investment Type:nk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.startup_funding].[cnt:Deals:qk]</rows>
        <cols>[federated.startup_funding].[yr:Date:ok]</cols>
      </table>
    </worksheet>

    <worksheet name='Top 15 Startups'>
      <layout-options>
        <title>
          <formatted-text>
            <run bold='true' fontcolor='#111827' fontname='Georgia' fontsize='14'>Top 15 funded startups</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='cleaned_indian_startup_funding' name='federated.startup_funding' />
          </datasources>
          <datasource-dependencies datasource='federated.startup_funding'>
            <column datatype='string' name='[Startup Name]' role='dimension' type='nominal' />
            <column datatype='string' name='[Industry Vertical]' role='dimension' type='nominal' />
            <column datatype='string' name='[City/Location]' role='dimension' type='nominal' />
            <column datatype='real' default-format='C1033,&quot;$&quot;#,##0;(&quot;$&quot;#,##0)' name='[Amount in USD]' role='measure' type='quantitative' />
            <column-instance column='[Startup Name]' derivation='None' name='[none:Startup Name:nk]' pivot='key' type='nominal' />
            <column-instance column='[Industry Vertical]' derivation='None' name='[none:Industry Vertical:nk]' pivot='key' type='nominal' />
            <column-instance column='[City/Location]' derivation='None' name='[none:City/Location:nk]' pivot='key' type='nominal' />
            <column-instance column='[Amount in USD]' derivation='Sum' name='[sum:Amount in USD:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Text' />
            <encodings>
              <text column='[federated.startup_funding].[sum:Amount in USD:qk]' />
              <color value='#B3541E' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.startup_funding].[none:Startup Name:nk]</rows>
        <cols>[federated.startup_funding].[none:Industry Vertical:nk]&#10;[federated.startup_funding].[none:City/Location:nk]</cols>
      </table>
    </worksheet>
  </worksheets>

  <dashboards>
    <dashboard name='Indian Startup Funding Landscape'>
      <style>
        <style-rule element='dashboard'>
          <format attr='color' value='#FFFFFF' />
        </style-rule>
      </style>
      <size maxheight='1700' maxwidth='1280' minheight='1700' minwidth='1280' type='fixed' />
      <zones>
        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>
          <zone h='98000' id='2' param='vert' type-v2='layout-flow' w='96000' x='2000' y='1000'>
            <zone h='5000' id='3' type-v2='title' w='96000'>
              <formatted-text>
                <run bold='true' fontcolor='#111827' fontname='Georgia' fontsize='24'>Indian Startup Funding Landscape (2015–2025)</run>
                <run fontcolor='#64748B' fontname='Arial' fontsize='12'>&#10;Sector trends, city ecosystems and stage-wise deal flow</run>
              </formatted-text>
            </zone>
            <zone h='8000' id='4' name='KPI Overview' type-v2='widget' w='96000' />
            <zone h='25000' id='5' param='horz' type-v2='layout-flow' w='96000'>
              <zone h='25000' id='6' name='Funding Trend' type-v2='widget' w='60000' />
              <zone h='25000' id='7' name='Sector Share' type-v2='widget' w='36000' />
            </zone>
            <zone h='25000' id='8' param='horz' type-v2='layout-flow' w='96000'>
              <zone h='25000' id='9' name='City Map' type-v2='widget' w='50000' />
              <zone h='25000' id='10' name='Stage Mix' type-v2='widget' w='46000' />
            </zone>
            <zone h='30000' id='11' name='Top 15 Startups' type-v2='widget' w='96000' />
          </zone>
        </zone>
      </zones>
    </dashboard>
  </dashboards>
  <windows saved-dpi-scale-factor='1.25' source-height='30'>
    <window class='dashboard' maximized='true' name='Indian Startup Funding Landscape'>
      <viewpoints />
      <active id='-1' />
    </window>
  </windows>
</workbook>
"""

twb_filename = 'Indian_Startup_Funding_Landscape.twb'
with open(twb_filename, 'w', encoding='utf-8') as f:
    f.write(twb_content)
print(f"Saved {twb_filename}")

# package into .twbx
twbx_filename = 'Indian_Startup_Funding_Landscape.twbx'
twbx_twb = twb_content.replace("directory='.'", "directory='Data'")

with zipfile.ZipFile(twbx_filename, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr(twb_filename, twbx_twb)
    z.write(csv_name, f'Data/{csv_name}')

print(f"Packaged {twbx_filename} ({os.path.getsize(twbx_filename)} bytes)")
