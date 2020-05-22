from lyra_orm.config import Base, session
from lyra_orm.models import Ura
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, Float


class ResultTest(Base):
    __tablename__ = "result_test"
    id = Column(String, primary_key=True)
    to_number = Column(String(20))
    label = Column(String(50))
    success = Column(Boolean())
    call_status = Column(String(30))
    transcription = Column(String(30))
    transcripted_text = Column(Text())
    transcripted_quality = Column(Float())
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    start_at = Column(DateTime())
    end_at = Column(DateTime())
    call_duration = Column(Integer())
    recording_duration = Column(Integer())
    recording_sid = Column(Text())
    recording_url = Column(Text())
    error_code = Column(Integer())
    alarmed_at = Column(DateTime())

    def json(self):
        return {
            "id": self.id,
            "to-number": self.to_number,
            "label": self.label,
            "success": self.success,
            "call-status": self.call_status,
            "transcription": self.transcription,
            "transcripted-text": self.transcripted_text,
            "transcripted-quality": self.transcripted_quality,
            "created-at": str(self.created_at),
            "updated-at": str(self.updated_at),
            "start-at": str(self.start_at),
            "end-at": str(self.end_at),
            "call-duration": self.call_duration,
            "recording-duration": self.recording_duration,
            "recording-sid": self.recording_sid,
            "recording-url": self.recording_url,
            "error-code": self.error_code,
            "alarmed_at": self.alarmed_at,
        }

    def minimal_json(self):
        return {
            "id": self.id,
            "to-number": self.to_number,
            "label": self.label,
            "success": self.success,
            "call-status": self.call_status,
            "transcription": self.transcription,
            "start-at": str(self.start_at),
            "recording-duration": self.recording_duration,
            "alarmed_at": self.alarmed_at,
        }

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).filter_by(id=id).one_or_none()

    @classmethod
    def find_by_to_number(cls, number, limit=3):
        return (
            session.query(cls)
            .filter_by(to_number=number)
            .order_by(ResultTest.start_at.desc())
            .limit(limit)
            .all()
        )

    @classmethod
    def find_all(cls):
        return session.query(cls).all()

    @classmethod
    def get_last_unlarmed_faileds(cls):
        unlarmeds = {}
        for ura in Ura.get_uras_numbers():
            results_obj = (
                session.query(cls)
                .filter_by(to_number=ura, success=False, alarmed_at=None)
                .order_by(ResultTest.start_at.desc())
                .all()
            )

            unlarmeds.update({ura: results_obj})

        return unlarmeds

    @classmethod
    def find_results(cls, uras=list(), n_last_results=3):
        results = {}
        uras = uras if uras else Ura.get_uras_numbers()

        for ura in uras:
            results_obj = ResultTest.find_by_to_number(ura, limit=n_last_results)
            test_results = [r.minimal_json() for r in results_obj]
            results.update({ura: test_results})

        return results

    def save_to_db(self):
        session.add(self)
        session.commit()
        session.close()

    def delete_from_db(self):
        session.delete(self)
        session.commit()
        session.close()
