from typing import Literal, Annotated
from typing_extensions import Doc

from hydrus.client.ClientParsing import PageParser, ContentParser, ParseFormulaJSON, ParseFormulaZipper, \
    ParseFormulaContextVariable
from hydrus.client.ClientStrings import StringMatch, StringConverter, StringProcessor
from hydrus.client.networking.ClientNetworkingGUG import GalleryURLGenerator
from hydrus.client.networking.ClientNetworkingURLClass import URLClass, URLClassParameterFixedName
from hydrus.core.HydrusConstants import ALL_SERVICES
from hydrus.core.HydrusSerialisable import SerialisableList

default = lambda x: x
path = lambda y, x: x


ProvidedServices = Literal["xxnx.com"]
ProvidedServicesDict = dict[
    Annotated[ProvidedServices, Doc("Service name")],
    Annotated[bytes, Doc("Service key")],
]

PROVIDED_SERVICES_IDS = {
    "xxnx.com": b'\xd0\xa2\xbd\x0b\xf3h\x0e\xc8cf\xa6fE^\x11\x9bud\x1c\x8ba+\x0e\xaap\xf4\xf9i\x93C\x95\x97',
}


def generate_stuff_payload(
    host: str,
    proto: str,
    services: ProvidedServicesDict,
):
    # HydrusYTDLProxy (url|file) — /dl -> the /dl endpoint on our server, being marked as file url
    # HydrusYTDLProxy (url|gallery) — /meta -> the /meta endpoint on our server, being marked as gallery 
    # HydrusYTDLProxy (url|post) — /meta -> the /meta endpoint on our server, being marked as post url
    # HydrusYTDLProxy (url|post) — xnxx.com file page (match-all) ->
    # HydrusYTDLProxy (parser) — /meta ->  
    # HydrusYTDLProxy (generator) — /meta -> 
    
    
    # HydrusYTDLProxy url <-> HydrusYTDLProxy (generator) — /meta
    # HydrusYTDLProxy (dl) <-> HydrusYTDLProxy (url class: dl) -> 
    # HydrusYTDLProxy (meta as gallery) <-> HydrusYTDLProxy (url class: meta as gallery) 
    # HydrusYTDLProxy — xnxx.com file page (match-all) <-> HydrusYTDLProxy (url class) — xnxx.com file page (match-all)
    # HydrusYTDLProxy (meta) <-> HydrusYTDLProxy (parser) — /meta

    return SerialisableList([
        path('hydrus.client.networking.ClientNetworkingURLClass.URLClass', URLClass(
            name='HydrusYTDLProxy (url|file) — /dl',
            url_class_key=b"\xb9\x1b\xe0\xfcZy\x0c9\x0fc\xfa\x9b\xa0\xfb\xb7G\xbc'\xd9;\x14\x1bv\xc9\xaf\nq\x8c\x02\x05\x15\x9b",
            url_type=2,  # FILE
            preferred_scheme=default('https'),
            netloc=host,
            path_components=[
                (
                    path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                        match_type=0,
                        match_value='dl',
                        min_chars=default(None),
                        max_chars=default(None),
                        example_string='dl',
                    )),
                    None
                )
            ],
            parameters=[
                path('hydrus.client.networking.ClientNetworkingURLClass.URLClassParameterFixedName',
                     URLClassParameterFixedName(
                         name='format',
                         value_string_match=path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                             match_type=1,
                             match_value=1,
                             min_chars=default(None),
                             max_chars=default(None),
                             example_string='value',
                         )),
                     )),
                path('hydrus.client.networking.ClientNetworkingURLClass.URLClassParameterFixedName',
                     URLClassParameterFixedName(
                         name='url',
                         value_string_match=path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                             match_type=2,
                             match_value='https?(:|%3A)(/|%2F)(/|%2F).+',
                             min_chars=default(None),
                             max_chars=default(None),
                             example_string='https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330',
                         )),
                     ))
            ],
            has_single_value_parameters=default(False),
            single_value_parameters_string_match=path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                match_type=default(3),
                match_value=default(''),
                min_chars=default(None),
                max_chars=default(None),
                example_string=default('example string'),
            )),
            header_overrides={
    
            },
            api_lookup_converter=path('hydrus.client.ClientStrings.StringConverter', StringConverter(
                conversions=[],
                example_string='https://hostname.com/post/page.php?id=123456&s=view',
            )),
            send_referral_url=default(0),
            referral_url_converter=path('hydrus.client.ClientStrings.StringConverter', StringConverter(
                conversions=[],
                example_string='https://hostname.com/post/page.php?id=123456&s=view',
            )),
            gallery_index_type=default(None),
            gallery_index_identifier=default(None),
            gallery_index_delta=default(1),
            example_url=f'{proto}://{host}/dl?url=https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330&format=best',
        )),
        path('hydrus.client.networking.ClientNetworkingURLClass.URLClass', URLClass(
            name='HydrusYTDLProxy (url|gallery) — /meta',
            url_class_key=b'\xdao\x8e\xa5\x0b\xb5\x90\xe7\xf7\x98h\x8b\xb7\nQ\xac>Q9\xe1\xe7\xa6*\x98\x8dn\xd7.e*\xec\x96',
            url_type=3,  # gallery
            preferred_scheme=default('https'),
            netloc=host,
            path_components=[
                (
                    path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                        match_type=0,
                        match_value='meta',
                        min_chars=default(None),
                        max_chars=default(None),
                        example_string='meta',
                    )),
                    None
                )
            ],
            parameters=[
                path('hydrus.client.networking.ClientNetworkingURLClass.URLClassParameterFixedName',
                     URLClassParameterFixedName(
                         name='url',
                         value_string_match=path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                             match_type=2,
                             match_value='https?(:|%3A)(/|%2F)(/|%2F).+',
                             min_chars=default(None),
                             max_chars=default(None),
                             example_string='https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330',
                         )),
                     ))
            ],
            has_single_value_parameters=default(False),
            single_value_parameters_string_match=path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                match_type=default(3),
                match_value=default(''),
                min_chars=default(None),
                max_chars=default(None),
                example_string=default('example string'),
            )),
            header_overrides={
    
            },
            api_lookup_converter=path('hydrus.client.ClientStrings.StringConverter', StringConverter(
                conversions=[],
                example_string='https://hostname.com/post/page.php?id=123456&s=view',
            )),
            send_referral_url=default(0),
            referral_url_converter=path('hydrus.client.ClientStrings.StringConverter', StringConverter(
                conversions=[],
                example_string='https://hostname.com/post/page.php?id=123456&s=view',
            )),
            gallery_index_type=default(None),
            gallery_index_identifier=default(None),
            gallery_index_delta=default(1),
            example_url=f'{proto}://{host}/meta?url=https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330',
        )),
        path('hydrus.client.networking.ClientNetworkingURLClass.URLClass', URLClass(
            name='HydrusYTDLProxy (url|post) — /meta',
            url_class_key=b'$)\x02\x8do\x00\xacd&a\xd8\xbf\xda\xfbk(,\xe9\xd46\xf1\xac\t\xb2\xb9\xec\x8e\x82s\xc3\xb3\xfb',
            url_type=0,
            preferred_scheme=default('https'),
            netloc=host,
            path_components=[
                (
                    path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                        match_type=0,
                        match_value='meta',
                        min_chars=default(None),
                        max_chars=default(None),
                        example_string='meta',
                    )),
                    None
                )
            ],
            parameters=[
                path('hydrus.client.networking.ClientNetworkingURLClass.URLClassParameterFixedName',
                     URLClassParameterFixedName(
                         name='url',
                         value_string_match=path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                             match_type=2,
                             match_value='https?(:|%3A)(/|%2F)(/|%2F).+',
                             min_chars=default(None),
                             max_chars=default(None),
                             example_string='https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330',
                         )),
                     ))
            ],
            has_single_value_parameters=default(False),
            single_value_parameters_string_match=path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                match_type=default(3),
                match_value=default(''),
                min_chars=default(None),
                max_chars=default(None),
                example_string=default('example string'),
            )),
            header_overrides={
    
            },
            api_lookup_converter=path('hydrus.client.ClientStrings.StringConverter', StringConverter(
                conversions=[],
                example_string='https://hostname.com/post/page.php?id=123456&s=view',
            )),
            send_referral_url=default(0),
            referral_url_converter=path('hydrus.client.ClientStrings.StringConverter', StringConverter(
                conversions=[],
                example_string='https://hostname.com/post/page.php?id=123456&s=view',
            )),
            gallery_index_type=default(None),
            gallery_index_identifier=default(None),
            gallery_index_delta=default(1),
            example_url=f'{proto}://{host}/meta?url=https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330',
        )),
        path('hydrus.client.ClientParsing.PageParser', PageParser(
            name='HydrusYTDLProxy (parser) — /meta',
            parser_key=b"\x87`\x80\x18\xb0-\xec*I\xd3t:p\x7f_\x91\xe1\xd0\x1d\x19\x1d\xe1\xe7\x81ic'\xb9\x8c\xd2\xb1\x86",
            string_converter=path('hydrus.client.ClientStrings.StringConverter', StringConverter(
                conversions=[],
                example_string='example string',
            )),
            sub_page_parsers=[],
            content_parsers=[
                path('hydrus.client.ClientParsing.ContentParser', ContentParser(
                    name='Note: Meta json',
                    content_type=18,
                    formula=path('hydrus.client.ClientParsing.ParseFormulaJSON', ParseFormulaJSON(
                        parse_rules=[
                            (
                                0,
                                path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                    match_type=0,
                                    match_value='meta',
                                    min_chars=default(None),
                                    max_chars=default(None),
                                    example_string='meta',
                                ))
                            )
                        ],
                        content_to_fetch=1,
                        name='',
                        string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                    )),
                    additional_info='ytdl meta json',
                )),
                path('hydrus.client.ClientParsing.ContentParser', ContentParser(
                    name='Tag: description:<extractor>:<…>',
                    content_type=0,
                    formula=path('hydrus.client.ClientParsing.ParseFormulaZipper', ParseFormulaZipper(
                        formulae=[
                            path('hydrus.client.ClientParsing.ParseFormulaJSON', ParseFormulaJSON(
                                parse_rules=[
                                    (
                                        0,
                                        path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                            match_type=0,
                                            match_value='meta',
                                            min_chars=default(None),
                                            max_chars=default(None),
                                            example_string='meta',
                                        ))
                                    ),
                                    (
                                        0,
                                        path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                            match_type=0,
                                            match_value='extractor',
                                            min_chars=default(None),
                                            max_chars=default(None),
                                            example_string='extractor',
                                        ))
                                    )
                                ],
                                content_to_fetch=0,
                                name='.meta.extractor',
                                string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                            )),
                            path('hydrus.client.ClientParsing.ParseFormulaJSON', ParseFormulaJSON(
                                parse_rules=[
                                    (
                                        0,
                                        path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                            match_type=0,
                                            match_value='description',
                                            min_chars=default(None),
                                            max_chars=default(None),
                                            example_string='description',
                                        ))
                                    )
                                ],
                                content_to_fetch=0,
                                name='.description',
                                string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                            ))
                        ],
                        sub_phrase='\\1:\\2',
                        name='',
                        string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                    )),
                    additional_info='description',
                )),
                path('hydrus.client.ClientParsing.ContentParser', ContentParser(
                    name='Tag: title:<extractor>:<…>',
                    content_type=0,
                    formula=path('hydrus.client.ClientParsing.ParseFormulaZipper', ParseFormulaZipper(
                        formulae=[
                            path('hydrus.client.ClientParsing.ParseFormulaJSON', ParseFormulaJSON(
                                parse_rules=[
                                    (
                                        0,
                                        path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                            match_type=0,
                                            match_value='meta',
                                            min_chars=default(None),
                                            max_chars=default(None),
                                            example_string='meta',
                                        ))
                                    ),
                                    (
                                        0,
                                        path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                            match_type=0,
                                            match_value='extractor',
                                            min_chars=default(None),
                                            max_chars=default(None),
                                            example_string='extractor',
                                        ))
                                    )
                                ],
                                content_to_fetch=0,
                                name='.meta.extractor',
                                string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                            )),
                            path('hydrus.client.ClientParsing.ParseFormulaJSON', ParseFormulaJSON(
                                parse_rules=[
                                    (
                                        0,
                                        path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                            match_type=0,
                                            match_value='title',
                                            min_chars=default(None),
                                            max_chars=default(None),
                                            example_string='title',
                                        ))
                                    )
                                ],
                                content_to_fetch=0,
                                name='.title',
                                string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                            ))
                        ],
                        sub_phrase='\\1:\\2',
                        name='',
                        string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                    )),
                    additional_info='title',
                )),
                path('hydrus.client.ClientParsing.ContentParser', ContentParser(
                    name='Tags: from api',
                    content_type=0,
                    formula=path('hydrus.client.ClientParsing.ParseFormulaJSON', ParseFormulaJSON(
                        parse_rules=[
                            (
                                0,
                                path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                    match_type=0,
                                    match_value='tags',
                                    min_chars=default(None),
                                    max_chars=default(None),
                                    example_string='tags',
                                ))
                            ),
                            (
                                1,
                                None
                            )
                        ],
                        content_to_fetch=0,
                        name='all tags as prepared by the api',
                        string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                    )),
                    additional_info=default(None),
                )),
                path('hydrus.client.ClientParsing.ContentParser', ContentParser(
                    name='URL: all the formats',
                    content_type=7,
                    formula=path('hydrus.client.ClientParsing.ParseFormulaJSON', ParseFormulaJSON(
                        parse_rules=[
                            (
                                0,
                                path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                    match_type=0,
                                    match_value='formats',
                                    min_chars=default(None),
                                    max_chars=default(None),
                                    example_string='formats',
                                ))
                            ),
                            (
                                1,
                                None
                            ),
                            (
                                0,
                                path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                    match_type=0,
                                    match_value='url',
                                    min_chars=default(None),
                                    max_chars=default(None),
                                    example_string='url',
                                ))
                            )
                        ],
                        content_to_fetch=0,
                        name='',
                        string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                    )),
                    additional_info=(
                        7,
                        50
                    ),
                )),
                path('hydrus.client.ClientParsing.ContentParser', ContentParser(
                    name='URL: best format',
                    content_type=7,
                    formula=path('hydrus.client.ClientParsing.ParseFormulaJSON', ParseFormulaJSON(
                        parse_rules=[
                            (
                                0,
                                path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                    match_type=0,
                                    match_value='formats',
                                    min_chars=default(None),
                                    max_chars=default(None),
                                    example_string='formats',
                                ))
                            ),
                            (
                                0,
                                path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                    match_type=0,
                                    match_value='best',
                                    min_chars=default(None),
                                    max_chars=default(None),
                                    example_string='best',
                                ))
                            ),
                            (
                                0,
                                path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                                    match_type=0,
                                    match_value='url',
                                    min_chars=default(None),
                                    max_chars=default(None),
                                    example_string='url',
                                ))
                            )
                        ],
                        content_to_fetch=0,
                        name='',
                        string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                    )),
                    additional_info=(
                        7,
                        75
                    ),
                )),
                path('hydrus.client.ClientParsing.ContentParser', ContentParser(
                    name='URL: the url provided via querystring',
                    content_type=7,
                    formula=path('hydrus.client.ClientParsing.ParseFormulaZipper', ParseFormulaZipper(
                        formulae=[
                            path('hydrus.client.ClientParsing.ParseFormulaContextVariable', ParseFormulaContextVariable(
                                variable_name='url',
                                name='param provided url',
                                string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                            ))
                        ],
                        sub_phrase='\\1',
                        name='param provided url',
                        string_processor=path('hydrus.client.ClientStrings.StringProcessor', StringProcessor()),
                    )),
                    additional_info=(
                        8,
                        100
                    ),
                ))
            ],
            example_urls=[
                f'{proto}://{host}/meta?url=https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330'
            ],
            example_parsing_context={
                'url': f'{proto}://{host}/meta?url=https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330'
            },
        )),
        path('hydrus.client.networking.ClientNetworkingGUG.GalleryURLGenerator', GalleryURLGenerator(
            name='HydrusYTDLProxy (generator) — /meta',
            gug_key=b'\xc9\xa5\x15\x9fAJ\x9c@\xdd\x14\xdf|\x1a\xea\xa9\xe9@\x7f\x8d\xa4\x08D\xa24<\xfb\xaf\xe4xWIx',
            url_template=f'{proto}://{host}/meta?url={{url}}',
            replacement_phrase='{url}',
            search_terms_separator='',
            initial_search_text='url to download',
            example_search_text='https://www.pornhub.com/view_video.php?viewkey=ph60df1d3ba7e51',
        )),
        *[
            select_existing_services(
                service=service_name,
                service_key=service_key,
                host=host,
                proto=proto,
            )
            for service_name, service_key in services.items()
        ],
    ])
# end def


def select_existing_services(
    service: ProvidedServices,
    service_key: bytes,
    host: str,
    proto: str,
):
    return {
        "xxnx.com": path('hydrus.client.networking.ClientNetworkingURLClass.URLClass', URLClass(
            name=f'HydrusYTDLProxy (url|post) — {service} file page (match-all)',
            url_class_key=service_key,
            url_type=0,
            preferred_scheme=default('https'),
            netloc='xnxx.com',
            path_components=[
                (
                    path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                        match_type=2,
                        match_value='^video-[a-z0-9]+$',
                        min_chars=default(None),
                        max_chars=default(None),
                        example_string='video-xg44xe4',
                    )),
                    None
                ),
                (
                    path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                        match_type=2,
                        match_value='^(?!video$).*(?<!^video)$',
                        min_chars=default(None),
                        max_chars=default(None),
                        example_string='foo',
                    )),
                    '%5BObject%20object%5D'
                )
            ],
            parameters=[],
            has_single_value_parameters=default(False),
            single_value_parameters_string_match=path('hydrus.client.ClientStrings.StringMatch', StringMatch(
                match_type=default(3),
                match_value=default(''),
                min_chars=default(None),
                max_chars=default(None),
                example_string=default('example string'),
            )),
            header_overrides={

            },
            api_lookup_converter=path('hydrus.client.ClientStrings.StringConverter', StringConverter(
                conversions=[
                    (
                        9,
                        (
                            '^(https?://(www\\.)?xnxx.com/video-[a-z0-9]+)(/.*)?$',
                            '\\1/video'
                        )
                    ),
                    (
                        4,
                        0
                    ),
                    (
                        2,
                        f'{proto}://{host}/meta?url='
                    )
                ],
                example_string='https://www.xnxx.com/video-xg44xe4/aubrey_star_19_year_old_solo_swimsuit_shiny_seamless_tights_cock_tease_jerk_off_encouragement_',
            )),
            send_referral_url=default(0),
            referral_url_converter=path('hydrus.client.ClientStrings.StringConverter', StringConverter(
                conversions=[],
                example_string='https://hostname.com/post/page.php?id=123456&s=view',
            )),
            gallery_index_type=default(None),
            gallery_index_identifier=default(None),
            gallery_index_delta=default(1),
            example_url='https://www.xnxx.com/video-xg44xe4/aubrey_star_19_year_old_solo_swimsuit_shiny_seamless_tights_cock_tease_jerk_off_encouragement_',
        )),
    }[service]
# end def
