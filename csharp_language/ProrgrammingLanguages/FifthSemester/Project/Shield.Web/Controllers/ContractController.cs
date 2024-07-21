using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

using Shield.Web.Data.Contexts;
using Shield.DataAccess.DTOs;
using Shield.DataAccess.Models;

using Microsoft.EntityFrameworkCore;

namespace Shield.Web.Controllers;

[Route("api/contract")]
[ApiController]
public class ContractController : ControllerBase
{
    private readonly DataContext _context;

    public ContractController(DataContext context) 
    { 
        _context = context;
    }

    [HttpGet]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> GetAllContracts()
    {
        return Ok(_context.Contracts.Include(c => c.Picture).Include(c => c.Alarms).Select(entity => new ContractDto()
        {
            ContractId = entity.ContractId,
            Address = entity.Address,
            Owners = entity.Owners,
            Bailee = entity.Bailee,
            Comment = entity.Comment,
            Organization = entity.Organization,
            SignDate = entity.SignDate,
            Picture = new PictureDto()
            {
                PictureId = entity.Picture.PictureId,
                Title = entity.Picture.Title,
                Type = entity.Picture.Type,
                Data = entity.Picture.Data
            },
            Alarms = entity.Alarms.Select(a => new AlarmDto()
            {
                AlarmId = a.AlarmId,
                Date = a.Date
            }).ToList()
        }).ToList());
    }

    [HttpPost]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> CreateContract([FromBody] ContractDto contract)
    {
        var c = new Contract
        {
            Address = contract.Address,
            Comment = contract.Comment,
            Owners = contract.Owners,
            Bailee = contract.Bailee,
            Organization = contract.Organization,
            SignDate = contract.SignDate
        };

        var plan = new Plan()
        {
            Title = contract.Plan.Title,
            Type = contract.Plan.Type,
            Data = contract.Plan.Data,
            Contract = c
        };

        var picture = new Picture()
        {
            Title = contract.Picture.Title,
            Type = contract.Picture.Type,
            Data = contract.Picture.Data,
            Contract = c
        };

        c.Plan = plan;
        c.Picture = picture;

        var entity = (await _context.Contracts.AddAsync(c)).Entity;
        //await _context.Plans.AddAsync(plan);
        //await _context.Pictures.AddAsync(picture);

        await _context.SaveChangesAsync();

        return Ok(new ContractDto()
        {
            ContractId = entity.ContractId,
            Address = entity.Address,
            Owners = entity.Owners,
            Bailee = entity.Bailee,
            Comment = entity.Comment,
            Organization = entity.Organization,
            SignDate = entity.SignDate,
            Plan = new PlanDto()
            {
                PlanId = entity.Plan.PlanId,
                Title = entity.Plan.Title,
                Type = entity.Plan.Type,
                Data = entity.Plan.Data
            },
            Picture = new PictureDto()
            {
                PictureId = entity.Picture.PictureId,
                Title = entity.Picture.Title,
                Type = entity.Picture.Type,
                Data = entity.Picture.Data
            }
        });
    }

    [HttpGet("{id}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> GetContractFull([FromRoute] int id)
    {
        var entity = await _context.Contracts.Include(c => c.Plan).Include(c => c.Picture).Include(c => c.Alarms).FirstOrDefaultAsync(c => c.ContractId == id);
        if (entity != null) return Ok(new ContractDto()
        {
            ContractId = entity.ContractId,
            Address = entity.Address,
            Owners = entity.Owners,
            Bailee = entity.Bailee,
            Comment = entity.Comment,
            Organization = entity.Organization,
            SignDate = entity.SignDate,
            Plan = new PlanDto()
            {
                PlanId = entity.Plan.PlanId,
                Title = entity.Plan.Title,
                Type = entity.Plan.Type,
                Data = entity.Plan.Data
            },
            Picture = new PictureDto()
            {
                PictureId = entity.Picture.PictureId,
                Title = entity.Picture.Title,
                Type = entity.Picture.Type,
                Data = entity.Picture.Data
            },
            Alarms = entity.Alarms.Select(a => new AlarmDto()
            {
                AlarmId = a.AlarmId,
                Date = a.Date
            }).ToList()
        });
        else return NotFound();
    }

    [HttpGet("{id}F")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> GetContract([FromRoute] int id)
    {
        var entity = await _context.Contracts.Include(c => c.Plan).Include(c => c.Picture).Include(c => c.Alarms).FirstOrDefaultAsync(c => c.ContractId == id);
        if (entity != null) return Ok(new ContractDto()
        {
            ContractId = entity.ContractId,
            Address = entity.Address,
            Owners = entity.Owners,
            Bailee = entity.Bailee,
            Comment = entity.Comment,
            Organization = entity.Organization,
            SignDate = entity.SignDate,
            Plan = new PlanDto()
            {
                PlanId = entity.Plan.PlanId,
                Title = entity.Plan.Title,
                Type = entity.Plan.Type,
                Data = entity.Plan.Data
            },
            Picture = new PictureDto()
            {
                PictureId = entity.Picture.PictureId,
                Title = entity.Picture.Title,
                Type = entity.Picture.Type,
                Data = entity.Picture.Data
            },
            Alarms = entity.Alarms.Select(a => new AlarmDto()
            {
                AlarmId = a.AlarmId,
                Date = a.Date
            }).ToList()
        });
        else return NotFound();
    }

    [HttpDelete("{id}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> DeleteContract([FromRoute] int id)
    {
        var contract = await _context.Contracts.FindAsync(id);
        if (contract != null)
        {
            _context.Contracts.Remove(contract);
            await _context.SaveChangesAsync();
            return Ok(contract);
        }
        else return NotFound();
    }

    [HttpPut("{id}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> UpdateContract([FromRoute] int id, [FromBody] UpdateContractDto dto)
    {
        var entity = await _context.Contracts.Include(c => c.Plan).Include(c => c.Picture).FirstOrDefaultAsync(c => c.ContractId == id);
        if (entity != null)
        {
            if (dto.Address != null && entity.Address != dto.Address) entity.Address = dto.Address;
            if (dto.Bailee != null && entity.Bailee != dto.Bailee) entity.Bailee = dto.Bailee;
            if (dto.Owners != null && entity.Owners != dto.Owners) entity.Owners = dto.Owners;
            if (dto.Comment != null && entity.Comment != dto.Comment) entity.Comment = dto.Comment;
            if (dto.Organization != null && entity.Organization != dto.Organization) entity.Organization = dto.Organization;

            if (dto.Plan != null)
            {
                var plan = new Plan()
                {
                    Title = dto.Plan.Title,
                    Type = dto.Plan.Type,
                    Data = dto.Plan.Data,
                    Contract = entity
                };

                entity.Plan = plan;
            }

            if (dto.Picture != null)
            {
                var picture = new Picture()
                {
                    Title = dto.Picture.Title,
                    Type = dto.Picture.Type,
                    Data = dto.Picture.Data,
                    Contract = entity
                };

                entity.Picture = picture;
            }

            await _context.SaveChangesAsync();

            return Ok(new ContractDto()
            {
                ContractId = entity.ContractId,
                Address = entity.Address,
                Owners = entity.Owners,
                Bailee = entity.Bailee,
                Comment = entity.Comment,
                Organization = entity.Organization,
                SignDate = entity.SignDate,
                Plan = new PlanDto()
                {
                    PlanId = entity.Plan.PlanId,
                    Title = entity.Plan.Title,
                    Type = entity.Plan.Type,
                    Data = entity.Plan.Data
                },
                Picture = new PictureDto()
                {
                    PictureId = entity.Picture.PictureId,
                    Title = entity.Picture.Title,
                    Type = entity.Picture.Type,
                    Data = entity.Picture.Data
                }
            });
        }
        else
        {
            return NotFound();
        }
    }
}
