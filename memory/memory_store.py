from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Input(Base):
    __tablename__ = 'inputs'
    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    classification = Column(String)
    input_metadata = Column(JSON)  # Renamed from metadata
    trace_id = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    traces = relationship('Trace', back_populates='input')

class ExtractedField(Base):
    __tablename__ = 'extracted_fields'
    id = Column(Integer, primary_key=True)
    input_id = Column(Integer, ForeignKey('inputs.id'))
    field_name = Column(String)
    field_value = Column(Text)
    input = relationship('Input')

class Action(Base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True)
    input_id = Column(Integer, ForeignKey('inputs.id'))
    action_type = Column(String)
    status = Column(String)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    input = relationship('Input')

class Trace(Base):
    __tablename__ = 'traces'
    id = Column(Integer, primary_key=True)
    input_id = Column(Integer, ForeignKey('inputs.id'))
    step = Column(String)
    detail = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    input = relationship('Input', back_populates='traces')

# SQLite setup
engine = create_engine('sqlite:///memory_store.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# --- Helper functions for logging and traceability ---
def log_input(source, classification, input_metadata=None):
    session = SessionLocal()
    trace_id = str(uuid.uuid4())
    input_obj = Input(source=source, classification=classification, input_metadata=input_metadata, trace_id=trace_id)
    session.add(input_obj)
    session.commit()
    session.refresh(input_obj)
    session.close()
    return input_obj.id, trace_id

def log_extracted_field(input_id, field_name, field_value):
    session = SessionLocal()
    ef = ExtractedField(input_id=input_id, field_name=field_name, field_value=str(field_value))
    session.add(ef)
    session.commit()
    session.close()

def log_action(input_id, action_type, status, response):
    session = SessionLocal()
    act = Action(input_id=input_id, action_type=action_type, status=status, response=response)
    session.add(act)
    session.commit()
    session.close()

def log_trace(input_id, step, detail):
    session = SessionLocal()
    tr = Trace(input_id=input_id, step=step, detail=detail)
    session.add(tr)
    session.commit()
    session.close()

def get_trace_by_trace_id(trace_id):
    session = SessionLocal()
    input_obj = session.query(Input).filter_by(trace_id=trace_id).first()
    if not input_obj:
        session.close()
        return None
    traces = session.query(Trace).filter_by(input_id=input_obj.id).all()
    trace_list = [{"step": t.step, "detail": t.detail, "timestamp": t.timestamp.isoformat()} for t in traces]
    session.close()
    return trace_list

def get_all_logs():
    session = SessionLocal()
    inputs = session.query(Input).all()
    logs = []
    for inp in inputs:
        logs.append({
            "id": inp.id,
            "source": inp.source,
            "timestamp": inp.timestamp.isoformat(),
            "classification": inp.classification,
            "trace_id": inp.trace_id
        })
    session.close()
    return logs 