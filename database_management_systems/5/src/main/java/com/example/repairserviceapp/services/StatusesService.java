package com.example.repairserviceapp.services;

import com.example.repairserviceapp.entities.Status;
import com.example.repairserviceapp.entities.StatusHistory;
import com.example.repairserviceapp.exceptions.EntityNotFoundException;
import com.example.repairserviceapp.repos.StatusesHistoryRepo;
import com.example.repairserviceapp.repos.StatusesRepo;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

@Service
@Transactional(readOnly = true)
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class StatusesService {

    private final StatusesRepo statusesRepo;
    private final StatusesHistoryRepo statusesHistoryRepo;

    public List<Status> readAll() {
        return statusesRepo.findAll();
    }

    public Status read(UUID id) {
        return statusesRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no status with this id"));
    }

    @Transactional
    public Status create(Status status) {
        status.setId(UUID.randomUUID());
        return statusesRepo.save(status);
    }

    @Transactional
    public Status update(UUID id, Status status) {
        statusesRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no status with this id"));
        status.setId(id);
        return statusesRepo.save(status);
    }

    @Transactional
    public Status delete(UUID id) {
        Status oldStatus = statusesRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no status with this id"));
        statusesRepo.delete(oldStatus);
        return oldStatus;
    }

    public List<StatusHistory> readAllHistory() {
        return statusesHistoryRepo.findAll();
    }

    @Transactional
    public StatusHistory restore(UUID statusId, OffsetDateTime timestamp) {

        StatusHistory historyMaster = statusesHistoryRepo
                .findByStatusIdAndTimestamp(statusId, timestamp)
                .orElseThrow(() -> new EntityNotFoundException(
                        "There is no status with this id " + statusId + " and this timestamp " + timestamp
                ));
        return statusesHistoryRepo.save(historyMaster);
    }
}
