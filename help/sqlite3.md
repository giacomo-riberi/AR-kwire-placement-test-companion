# merge tables TEST and PA
```
SELECT TEST.*, PA.*
FROM TEST
LEFT JOIN PA ON TEST.id = PA.TEST_id;
```
