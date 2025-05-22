from typing import Dict, Any, List
from refiner.models.refined import Base
from refiner.transformer.base_transformer import DataTransformer
from refiner.models.refined import PreferencesRefined
from refiner.models.unrefined import PreferencesUnrefined
from refiner.utils.date import parse_timestamp
from refiner.utils.pii import mask_email
import json
from datetime import datetime

class DatapigTransformer(DataTransformer):
    """
    Transformer for user data as defined in the example.
    """
    
    def transform(self, data: Dict[str, Any]) -> List[Base]:
        """
        Transform raw user data into SQLAlchemy model instances.
        
        Args:
            data: Dictionary containing user data
            
        Returns:
            List of SQLAlchemy model instances
        """
        # Validate data with Pydantic
        unrefined_data = PreferencesUnrefined.model_validate(data)

        # return None
        
        # Create user instance
        preferences = PreferencesRefined(
            address=unrefined_data.address,
            unixtime=unrefined_data.unixtime,
            preferences=json.dumps(unrefined_data.preferences.model_dump()),
        )
        
        models = [preferences]
        
        # if unrefined_user.storage:
        #     storage_metric = StorageMetric(
        #         user_id=unrefined_user.userId,
        #         percent_used=unrefined_user.storage.percentUsed,
        #         recorded_at=created_at
        #     )
        #     models.append(storage_metric)
        
        # if unrefined_user.metadata:
        #     collection_date = parse_timestamp(unrefined_user.metadata.collectionDate)
        #     auth_source = AuthSource(
        #         user_id=unrefined_user.userId,
        #         source=unrefined_user.metadata.source,
        #         collection_date=collection_date,
        #         data_type=unrefined_user.metadata.dataType
        #     )
        #     models.append(auth_source)
        
        return models