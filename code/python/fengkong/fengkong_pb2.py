# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fengkong.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='fengkong.proto',
  package='fengkong',
  syntax='proto3',
  serialized_pb=_b('\n\x0e\x66\x65ngkong.proto\x12\x08\x66\x65ngkong\"\x17\n\x07\x44\x61taReq\x12\x0c\n\x04text\x18\x01 \x01(\t\"&\n\x08\x44\x61taResp\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0e\n\x06result\x18\x02 \x01(\x05\x32\x43\n\tFKPredict\x12\x36\n\x0b\x43\x61rdPredict\x12\x11.fengkong.DataReq\x1a\x12.fengkong.DataResp\"\x00\x62\x06proto3')
)




_DATAREQ = _descriptor.Descriptor(
  name='DataReq',
  full_name='fengkong.DataReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='fengkong.DataReq.text', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=51,
)


_DATARESP = _descriptor.Descriptor(
  name='DataResp',
  full_name='fengkong.DataResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='fengkong.DataResp.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result', full_name='fengkong.DataResp.result', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=53,
  serialized_end=91,
)

DESCRIPTOR.message_types_by_name['DataReq'] = _DATAREQ
DESCRIPTOR.message_types_by_name['DataResp'] = _DATARESP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DataReq = _reflection.GeneratedProtocolMessageType('DataReq', (_message.Message,), dict(
  DESCRIPTOR = _DATAREQ,
  __module__ = 'fengkong_pb2'
  # @@protoc_insertion_point(class_scope:fengkong.DataReq)
  ))
_sym_db.RegisterMessage(DataReq)

DataResp = _reflection.GeneratedProtocolMessageType('DataResp', (_message.Message,), dict(
  DESCRIPTOR = _DATARESP,
  __module__ = 'fengkong_pb2'
  # @@protoc_insertion_point(class_scope:fengkong.DataResp)
  ))
_sym_db.RegisterMessage(DataResp)



_FKPREDICT = _descriptor.ServiceDescriptor(
  name='FKPredict',
  full_name='fengkong.FKPredict',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=93,
  serialized_end=160,
  methods=[
  _descriptor.MethodDescriptor(
    name='CardPredict',
    full_name='fengkong.FKPredict.CardPredict',
    index=0,
    containing_service=None,
    input_type=_DATAREQ,
    output_type=_DATARESP,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_FKPREDICT)

DESCRIPTOR.services_by_name['FKPredict'] = _FKPREDICT

# @@protoc_insertion_point(module_scope)
