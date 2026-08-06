// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SecureWipeLedger {
    struct WipeRecord {
        string reportId;
        string deviceSerial;
        string wipeMethod;
        uint256 confidenceScore;
        uint256 timestamp;
        string certificateHash;
    }

    // Mapping from the unique block/certificate hash to the record
    mapping(string => WipeRecord) public records;
    // Keep track of hashes to check existence easily
    mapping(string => bool) public recordExists;

    event RecordAnchored(
        string indexed certificateHash,
        string reportId,
        string deviceSerial,
        uint256 timestamp
    );

    function anchorRecord(
        string memory _reportId,
        string memory _deviceSerial,
        string memory _wipeMethod,
        uint256 _confidenceScore,
        uint256 _timestamp,
        string memory _certificateHash
    ) public {
        require(!recordExists[_certificateHash], "Record with this hash already exists on-chain");

        records[_certificateHash] = WipeRecord({
            reportId: _reportId,
            deviceSerial: _deviceSerial,
            wipeMethod: _wipeMethod,
            confidenceScore: _confidenceScore,
            timestamp: _timestamp,
            certificateHash: _certificateHash
        });

        recordExists[_certificateHash] = true;

        emit RecordAnchored(_certificateHash, _reportId, _deviceSerial, _timestamp);
    }

    function verifyRecord(string memory _certificateHash) public view returns (
        bool exists,
        string memory reportId,
        string memory deviceSerial,
        string memory wipeMethod,
        uint256 confidenceScore,
        uint256 timestamp
    ) {
        exists = recordExists[_certificateHash];
        if (exists) {
            WipeRecord memory r = records[_certificateHash];
            return (true, r.reportId, r.deviceSerial, r.wipeMethod, r.confidenceScore, r.timestamp);
        } else {
            return (false, "", "", "", 0, 0);
        }
    }
}
