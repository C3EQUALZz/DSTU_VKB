package com.example.repairserviceapp.services;

import com.example.repairserviceapp.entities.Master;
import com.example.repairserviceapp.entities.MasterHistory;
import com.example.repairserviceapp.exceptions.EntityAlreadyExistsException;
import com.example.repairserviceapp.exceptions.EntityNotFoundException;
import com.example.repairserviceapp.repos.MastersHistoryRepo;
import com.example.repairserviceapp.repos.MastersRepo;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Example;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;


@Service
@Transactional(readOnly = true)
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class MastersService {

    private final MastersRepo mastersRepo;
    private final MastersHistoryRepo mastersHistoryRepo;

    public List<Master> readAll() {
        return mastersRepo.findAll();
    }

    public Master read(UUID id) {
        return mastersRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no master with this id"));
    }

    @Transactional
    public Master create(Master master) {
        if (exists(master.getName(), master.getSurname(), master.getPatronymic())) {
            throw new EntityAlreadyExistsException("This master already exists");
        }
        master.setId(UUID.randomUUID());
        return mastersRepo.save(master);
    }

    @Transactional
    public Master update(UUID id, Master master) {
        mastersRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no master with this id"));
        master.setId(id);
        return mastersRepo.save(master);
    }

    @Transactional
    public Master delete(UUID id) {
        Master oldMaster = mastersRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no master with this id"));
        mastersRepo.deleteById(id);
        return oldMaster;
    }

    public boolean exists(String name, String surname, String patronymic) {
        return mastersRepo.exists(Example.of(
                Master.builder().name(name).surname(surname).patronymic(patronymic).build()
        ));
    }

    public List<MasterHistory> readAllHistory() {
        return mastersHistoryRepo.findAll();
    }

    @Transactional
    public MasterHistory restore(UUID masterId, OffsetDateTime timestamp) {

        MasterHistory historyMaster = mastersHistoryRepo
                .findByMasterIdAndTimestamp(masterId, timestamp)
                .orElseThrow(() -> new EntityNotFoundException(
                        "There is no master with this id " + masterId + " and this timestamp " + timestamp
                ));

        return mastersRepo.save(historyMaster);
    }
}
