from pathlib import Path

from fraud_detection_model.config.core import (
    create_and_validate_config,
    fetch_config_from_yaml,
)

import pytest
from pydantic import ValidationError

TEST_CONFIG_TEXT = """
package_name: fraud_detection_model
pipeline_name: fraud_detection_model
pipeline_save_file: fraud_detection_model_output_v
train_transaction: train_transaction.csv
test_transaction: test_transaction.csv
train_identity: train_identity.csv
test_identity: test_identity.csv
target: isFraud
id: TransactionID
train_transaction_usecols:
  - TransactionID
  - C3
  - V13
  - V14
  - V15
  - V16
  - V17
  - V18
  - V19
  - V27
  - V28
  - V32
  - V98
  - V116
  - V117
  - V118
  - V119
  - V120
  - V153
  - V154
  - V157
  - V158
  - V235
  - V284
  - V286
  - V297
  - V300
  - V301
  - V302
  - V303
  - V304
  - V305
  - V325
  - V327
  - V328
  - TransactionDT
  - TransactionAmt
  - C1
  - C2
  - C4
  - C5
  - C6
  - C7
  - C8
  - C9
  - C10
  - C11
  - C12
  - C13
  - C14
  - V95
  - V96
  - V97
  - V99
  - V100
  - V101
  - V102
  - V126
  - V127
  - V145
  - V166
  - V279
  - V280
  - V285
  - V287
  - V290
  - V291
  - V292
  - V293
  - V294
  - V295
  - V298
  - V299
  - V306
  - V307
  - V308
  - V309
  - V310
  - V311
  - V312
  - V313
  - V316
  - V317
  - V318
  - V319
  - V320
  - V321
  - V322
  - V323
  - V324
  - V326
  - V329
  - V330
  - V331
  - V332
  - V333
  - V334
  - V335
  - V336
  - V337
  - V338
  - V339
  - R_emaildomain
  - card1
  - card2
  - card3
  - card5
  - addr1
  - addr2
  - ProductCD
  - isFraud
train_identity_usecols:
  - TransactionID
  - id_08
  - id_13
  - id_17
  - id_19
  - id_20
  - id_21
  - id_26
  - id_16
  - id_27
  - DeviceInfo
test_transaction_usecols:
  - TransactionID
  - C3
  - V13
  - V14
  - V15
  - V16
  - V17
  - V18
  - V19
  - V27
  - V28
  - V32
  - V98
  - V116
  - V117
  - V118
  - V119
  - V120
  - V153
  - V154
  - V157
  - V158
  - V235
  - V284
  - V286
  - V297
  - V300
  - V301
  - V302
  - V303
  - V304
  - V305
  - V325
  - V327
  - V328
  - TransactionDT
  - TransactionAmt
  - C1
  - C2
  - C4
  - C5
  - C6
  - C7
  - C8
  - C9
  - C10
  - C11
  - C12
  - C13
  - C14
  - V95
  - V96
  - V97
  - V99
  - V100
  - V101
  - V102
  - V126
  - V127
  - V145
  - V166
  - V279
  - V280
  - V285
  - V287
  - V290
  - V291
  - V292
  - V293
  - V294
  - V295
  - V298
  - V299
  - V306
  - V307
  - V308
  - V309
  - V310
  - V311
  - V312
  - V313
  - V316
  - V317
  - V318
  - V319
  - V320
  - V321
  - V322
  - V323
  - V324
  - V326
  - V329
  - V330
  - V331
  - V332
  - V333
  - V334
  - V335
  - V336
  - V337
  - V338
  - V339
  - R_emaildomain
  - card1
  - card2
  - card3
  - card5
  - addr1
  - addr2
  - ProductCD
test_identity_usecols:
  - TransactionID
  - id-08
  - id-13
  - id-17
  - id-19
  - id-20
  - id-21
  - id-26
  - id-16
  - id-27
  - DeviceInfo
test_features_to_rename:
  id-08: id_08
  id-13: id_13
  id-17: id_17
  id-19: id_19
  id-20: id_20
  id-21: id_21
  id-26: id_26
  id-16: id_16
  id-27: id_27
discrete_features:
  - V13
  - V14
  - V15
  - V16
  - V17
  - V18
  - V19
  - V27
  - V28
  - V32
  - V98
  - V116
  - V117
  - V118
  - V119
  - V120
  - V297
  - V300
  - V301
  - V325
  - V328
continuous_features:
  - TransactionDT
  - TransactionAmt
  - C1
  - C2
  - C3
  - C4
  - C5
  - C6
  - C7
  - C8
  - C9
  - C10
  - C11
  - C12
  - C13
  - C14
  - V97
  - V99
  - V100
  - V101
  - V102
  - V126
  - V127
  - V153
  - V154
  - V157
  - V158
  - V166
  - V293
  - V294
  - V306
  - V307
  - V308
  - V310
  - V311
  - V312
  - V313
  - V316
  - V317
  - V318
  - V319
  - V320
  - V321
  - V324
  - V326
  - V327
  - V329
  - V330
  - V331
  - V332
  - V336
high_cardinality_cats:
  - R_emaildomain
  - card1
  - card2
  - card3
  - card5
  - addr1
  - addr2
  - id_13
  - id_17
  - id_19
  - id_20
  - id_21
  - id_26
convert_to_category_codes:
  - ProductCD
  - R_emaildomain
  - card1
  - card2
  - card3
  - card5
  - addr1
  - addr2
  - id_13
  - id_17
  - id_19
  - id_20
  - id_21
  - id_26
impute_most_freq_cols:
  - R_emaildomain
  - card2
  - card3
  - card5
  - addr1
  - addr2
  - id_13
  - id_17
  - id_19
  - id_20
  - id_21
  - id_26
  - V13
  - V14
  - V15
  - V16
  - V17
  - V18
  - V19
  - V27
  - V28
  - V32
  - V98
  - V116
  - V117
  - V118
  - V119
  - V120
  - V297
  - V300
  - V301
  - V325
  - V328
all_features:
  - V13
  - V14
  - V15
  - V16
  - V17
  - V18
  - V19
  - V27
  - V28
  - V32
  - V98
  - V116
  - V117
  - V118
  - V119
  - V120
  - V297
  - V300
  - V301
  - V325
  - V328
  - TransactionDT
  - TransactionAmt
  - C1
  - C2
  - C3
  - C4
  - C5
  - C6
  - C7
  - C8
  - C9
  - C10
  - C11
  - C12
  - C13
  - C14
  - V97
  - V99
  - V100
  - V101
  - V102
  - V126
  - V127
  - V153
  - V154
  - V157
  - V158
  - V166
  - V293
  - V294
  - V306
  - V307
  - V308
  - V310
  - V311
  - V312
  - V313
  - V316
  - V317
  - V318
  - V319
  - V320
  - V321
  - V324
  - V326
  - V327
  - V329
  - V330
  - V331
  - V332
  - V336
  - R_emaildomain
  - card1
  - card2
  - card3
  - card5
  - addr1
  - addr2
  - id_13
  - id_17
  - id_19
  - id_20
  - id_21
  - id_26
  - ProductCD
random_state: 25
test_size: 0.33
n_estimators: 100
n_jobs: -1
"""

def test_fetch_config_structure(tmpdir):
    # Given
    # We make use of the pytest built-in tmpdir fixture
    configs_dir = Path(tmpdir)
    config_1 = configs_dir / "sample_config.yml"
    config_1.write_text(TEST_CONFIG_TEXT)
    parsed_config = fetch_config_from_yaml(cfg_path=config_1)

    # When
    config = create_and_validate_config(parsed_config=parsed_config)

    # Then
    assert config.model_config
    assert config.app_config


def test_missing_config_field_raises_validation_error(tmpdir):
    # Given
    # We make use of the pytest built-in tmpdir fixture
    configs_dir = Path(tmpdir)
    config_1 = configs_dir / "sample_config.yml"
    TEST_CONFIG_TEXT = """package_name: fraud_detection_model"""
    config_1.write_text(TEST_CONFIG_TEXT)
    parsed_config = fetch_config_from_yaml(cfg_path=config_1)

    # When
    with pytest.raises(ValidationError) as excinfo:
        create_and_validate_config(parsed_config=parsed_config)

    # Then
    assert "field required" in str(excinfo.value)
    assert "pipeline_name" in str(excinfo.value)