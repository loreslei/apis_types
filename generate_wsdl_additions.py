import re

with open('db/music.wsdl', 'r', encoding='utf-8') as f:
    wsdl = f.read()

# Add to <schema>
schema_additions = '''
            <xsd:complexType name="MutationResponse">
                <xsd:sequence>
                    <xsd:element name="success" type="xsd:boolean"/>
                    <xsd:element name="message" type="xsd:string"/>
                </xsd:sequence>
            </xsd:complexType>

            <!-- User CRUD -->
            <xsd:element name="CreateUserRequest">
                <xsd:complexType><xsd:sequence>
                    <xsd:element name="name" type="xsd:string"/>
                    <xsd:element name="age" type="xsd:int"/>
                </xsd:sequence></xsd:complexType>
            </xsd:element>
            <xsd:element name="UpdateUserRequest">
                <xsd:complexType><xsd:sequence>
                    <xsd:element name="id" type="xsd:int"/>
                    <xsd:element name="name" type="xsd:string"/>
                    <xsd:element name="age" type="xsd:int"/>
                </xsd:sequence></xsd:complexType>
            </xsd:element>
            <xsd:element name="DeleteUserRequest">
                <xsd:complexType><xsd:sequence><xsd:element name="id" type="xsd:int"/></xsd:sequence></xsd:complexType>
            </xsd:element>

            <!-- Song CRUD -->
            <xsd:element name="CreateSongRequest">
                <xsd:complexType><xsd:sequence>
                    <xsd:element name="name" type="xsd:string"/>
                    <xsd:element name="artist" type="xsd:string"/>
                </xsd:sequence></xsd:complexType>
            </xsd:element>
            <xsd:element name="UpdateSongRequest">
                <xsd:complexType><xsd:sequence>
                    <xsd:element name="id" type="xsd:int"/>
                    <xsd:element name="name" type="xsd:string"/>
                    <xsd:element name="artist" type="xsd:string"/>
                </xsd:sequence></xsd:complexType>
            </xsd:element>
            <xsd:element name="DeleteSongRequest">
                <xsd:complexType><xsd:sequence><xsd:element name="id" type="xsd:int"/></xsd:sequence></xsd:complexType>
            </xsd:element>

            <!-- Playlist CRUD -->
            <xsd:element name="CreatePlaylistRequest">
                <xsd:complexType><xsd:sequence>
                    <xsd:element name="name" type="xsd:string"/>
                    <xsd:element name="userId" type="xsd:int"/>
                </xsd:sequence></xsd:complexType>
            </xsd:element>
            <xsd:element name="UpdatePlaylistRequest">
                <xsd:complexType><xsd:sequence>
                    <xsd:element name="id" type="xsd:int"/>
                    <xsd:element name="name" type="xsd:string"/>
                </xsd:sequence></xsd:complexType>
            </xsd:element>
            <xsd:element name="DeletePlaylistRequest">
                <xsd:complexType><xsd:sequence><xsd:element name="id" type="xsd:int"/></xsd:sequence></xsd:complexType>
            </xsd:element>

            <!-- PlaylistSong CRUD -->
            <xsd:element name="AddSongToPlaylistRequest">
                <xsd:complexType><xsd:sequence>
                    <xsd:element name="playlistId" type="xsd:int"/>
                    <xsd:element name="songId" type="xsd:int"/>
                </xsd:sequence></xsd:complexType>
            </xsd:element>
            <xsd:element name="RemoveSongFromPlaylistRequest">
                <xsd:complexType><xsd:sequence>
                    <xsd:element name="playlistId" type="xsd:int"/>
                    <xsd:element name="songId" type="xsd:int"/>
                </xsd:sequence></xsd:complexType>
            </xsd:element>

            <xsd:element name="MutationResponseElement">
                <xsd:complexType><xsd:sequence>
                    <xsd:element name="success" type="xsd:boolean"/>
                    <xsd:element name="message" type="xsd:string"/>
                </xsd:sequence></xsd:complexType>
            </xsd:element>
'''
wsdl = wsdl.replace('</xsd:schema>', schema_additions + '</xsd:schema>')

messages = '''
    <message name="MutationResponseMsg"><part name="parameters" element="tns:MutationResponseElement"/></message>
'''
ops = ['CreateUser', 'UpdateUser', 'DeleteUser', 'CreateSong', 'UpdateSong', 'DeleteSong', 'CreatePlaylist', 'UpdatePlaylist', 'DeletePlaylist', 'AddSongToPlaylist', 'RemoveSongFromPlaylist']
for op in ops:
    messages += f'    <message name="{op}RequestMsg"><part name="parameters" element="tns:{op}Request"/></message>\n'

wsdl = wsdl.replace('</types>', '</types>\n' + messages)

portTypes = ''
for op in ops:
    portTypes += f'''        <operation name="{op}">
            <input message="tns:{op}RequestMsg"/>
            <output message="tns:MutationResponseMsg"/>
        </operation>\n'''

wsdl = wsdl.replace('</portType>', portTypes + '</portType>')

bindings = ''
for op in ops:
    bindings += f'''        <operation name="{op}">
            <soap:operation soapAction="http://example.com/music/{op}"/>
            <input><soap:body use="literal"/></input>
            <output><soap:body use="literal"/></output>
        </operation>\n'''

wsdl = wsdl.replace('</binding>', bindings + '</binding>')

with open('db/music.wsdl', 'w', encoding='utf-8') as f:
    f.write(wsdl)

print('WSDL updated successfully')
