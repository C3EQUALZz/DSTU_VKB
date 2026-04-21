import { useEffect, useState } from "react";

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || "/api/v1").replace(/\/$/, "");
const healthUrl = import.meta.env.VITE_HEALTH_URL || "/health";
const predictionHistoryLimit = 10;
const databaseRowsLimit = 10;

const emptyState = {
  label: "",
  confidence: 0,
  probabilities: {},
};

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [prediction, setPrediction] = useState(emptyState);
  const [predictionHistory, setPredictionHistory] = useState([]);
  const [databaseTables, setDatabaseTables] = useState([]);
  const [serviceStatus, setServiceStatus] = useState("checking");
  const [isDragging, setIsDragging] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isHistoryLoading, setIsHistoryLoading] = useState(true);
  const [isDatabaseLoading, setIsDatabaseLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [historyErrorMessage, setHistoryErrorMessage] = useState("");
  const [databaseErrorMessage, setDatabaseErrorMessage] = useState("");

  useEffect(() => {
    let active = true;

    fetch(healthUrl)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("backend unavailable");
        }
        const payload = await response.json();
        if (active) {
          setServiceStatus(payload.status);
        }
      })
      .catch(() => {
        if (active) {
          setServiceStatus("offline");
        }
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;

    fetchDatabaseTables(databaseRowsLimit)
      .then((payload) => {
        if (active) {
          setDatabaseTables(payload);
          setDatabaseErrorMessage("");
        }
      })
      .catch((error) => {
        if (active) {
          setDatabaseErrorMessage(error.message || "Не удалось загрузить таблицы базы данных.");
        }
      })
      .finally(() => {
        if (active) {
          setIsDatabaseLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;

    fetchPredictionHistory(predictionHistoryLimit)
      .then((payload) => {
        if (active) {
          setPredictionHistory(payload);
          setHistoryErrorMessage("");
        }
      })
      .catch((error) => {
        if (active) {
          setHistoryErrorMessage(error.message || "Не удалось загрузить историю запросов.");
        }
      })
      .finally(() => {
        if (active) {
          setIsHistoryLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl("");
      return undefined;
    }

    const localPreview = URL.createObjectURL(selectedFile);
    setPreviewUrl(localPreview);

    return () => {
      URL.revokeObjectURL(localPreview);
    };
  }, [selectedFile]);

  function handleFileChange(file) {
    if (!file) {
      return;
    }

    setErrorMessage("");
    setPrediction(emptyState);
    setSelectedFile(file);
  }

  async function refreshPredictionHistory() {
    setIsHistoryLoading(true);

    try {
      const payload = await fetchPredictionHistory(predictionHistoryLimit);
      setPredictionHistory(payload);
      setHistoryErrorMessage("");
    } catch (error) {
      setHistoryErrorMessage(error.message || "Не удалось обновить историю запросов.");
    } finally {
      setIsHistoryLoading(false);
    }
  }

  async function refreshDatabaseTables() {
    setIsDatabaseLoading(true);

    try {
      const payload = await fetchDatabaseTables(databaseRowsLimit);
      setDatabaseTables(payload);
      setDatabaseErrorMessage("");
    } catch (error) {
      setDatabaseErrorMessage(error.message || "Не удалось обновить таблицы базы данных.");
    } finally {
      setIsDatabaseLoading(false);
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!selectedFile) {
      setErrorMessage("Сначала выбери изображение.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setIsSubmitting(true);
    setErrorMessage("");

    try {
      const response = await fetch(`${apiBaseUrl}/predict`, {
        method: "POST",
        body: formData,
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Не удалось распознать изображение.");
      }

      setPrediction(payload);
      await refreshPredictionHistory();
      await refreshDatabaseTables();
    } catch (error) {
      setPrediction(emptyState);
      setErrorMessage(error.message || "Ошибка запроса.");
    } finally {
      setIsSubmitting(false);
    }
  }

  function onDrop(event) {
    event.preventDefault();
    setIsDragging(false);
    handleFileChange(event.dataTransfer.files?.[0] || null);
  }

  const rankedProbabilities = Object.entries(prediction.probabilities).sort((left, right) => right[1] - left[1]);

  return (
    <div className="app-shell">
      <div className="aurora aurora-left" />
      <div className="aurora aurora-right" />

      <main className="layout">
        <section className="hero-card">
          <div className="hero-header">
            <span className="eyebrow">Neural Figure Detector</span>
            <span className={`status-pill status-${serviceStatus}`}>{statusLabel(serviceStatus)}</span>
          </div>

          <h1>Shape Vision</h1>
          <p className="hero-copy">
            Загрузи изображение, а интерфейс покажет, какая геометрическая фигура на нём обнаружена и с какой уверенностью
            модель приняла решение.
          </p>

          <div className="shape-showcase" aria-hidden="true">
            <div className="shape-token circle-token" />
            <div className="shape-token triangle-token" />
            <div className="shape-token square-token" />
          </div>

          <div className="facts-grid">
            <article>
              <span>Classes</span>
              <strong>Circle / Triangle / Square</strong>
            </article>
            <article>
              <span>Flow</span>
              <strong>Upload -&gt; Predict -&gt; Store</strong>
            </article>
            <article>
              <span>Storage</span>
              <strong>SQLite + Alembic</strong>
            </article>
            <article>
              <span>Records</span>
              <strong>{isHistoryLoading ? "Loading..." : `${predictionHistory.length} latest rows`}</strong>
            </article>
            <article>
              <span>Tables</span>
              <strong>{isDatabaseLoading ? "Loading..." : `${databaseTables.length} database tables`}</strong>
            </article>
          </div>
        </section>

        <section className="panel-card">
          <form className="upload-form" onSubmit={handleSubmit}>
            <label
              className={`dropzone ${isDragging ? "dropzone-active" : ""} ${previewUrl ? "dropzone-has-image" : ""}`}
              onDragOver={(event) => {
                event.preventDefault();
                setIsDragging(true);
              }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={onDrop}
            >
              <input
                type="file"
                accept="image/*"
                onChange={(event) => handleFileChange(event.target.files?.[0] || null)}
              />

              {previewUrl ? (
                <div className="preview-frame">
                  <img src={previewUrl} alt="Предпросмотр загруженного изображения" className="preview-image" />
                </div>
              ) : (
                <div className="dropzone-copy">
                  <span className="dropzone-icon">▲</span>
                  <strong>Перетащи изображение сюда</strong>
                  <span>или нажми, чтобы выбрать файл</span>
                </div>
              )}
            </label>

            <div className="form-actions">
              <button type="submit" className="primary-button" disabled={isSubmitting}>
                {isSubmitting ? "Анализ..." : "Распознать фигуру"}
              </button>
              <p className="form-hint">Поддерживаются файлы, которые умеет читать Pillow: JPG, PNG и другие.</p>
            </div>
          </form>

          <section className="result-card">
            <div className="result-header">
              <span className="eyebrow">Result</span>
              {prediction.label ? <strong>{humanizeLabel(prediction.label)}</strong> : <strong>Ожидание запроса</strong>}
            </div>

            {errorMessage ? <p className="error-banner">{errorMessage}</p> : null}

            {prediction.label ? (
              <>
                <div className="confidence-meter">
                  <span>Уверенность модели</span>
                  <strong>{formatPercent(prediction.confidence)}</strong>
                </div>

                <div className="probability-list">
                  {rankedProbabilities.map(([label, probability]) => (
                    <div className="probability-row" key={label}>
                      <div className="probability-meta">
                        <span>{humanizeLabel(label)}</span>
                        <span>{formatPercent(probability)}</span>
                      </div>
                      <div className="probability-track">
                        <div className="probability-fill" style={{ width: `${probability * 100}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <p className="placeholder-copy">
                После отправки изображения здесь появится итоговая фигура и распределение вероятностей по всем классам.
              </p>
            )}
          </section>

          <section className="history-card">
            <div className="history-header">
              <div>
                <span className="eyebrow">Database</span>
                <h2>История запросов</h2>
              </div>

              <div className="history-meta">
                <strong>{predictionHistory.length}</strong>
                <span>последних записей</span>
              </div>
            </div>

            <p className="history-copy">
              Таблица показывает последние сохранённые записи из базы данных: файл, результат распознавания, уверенность
              модели и время запроса.
            </p>

            {historyErrorMessage ? <p className="error-banner">{historyErrorMessage}</p> : null}

            <div className="table-shell">
              {isHistoryLoading ? (
                <p className="history-placeholder">Загрузка истории из базы данных...</p>
              ) : predictionHistory.length > 0 ? (
                <table className="history-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Дата</th>
                      <th>Файл</th>
                      <th>Фигура</th>
                      <th>Уверенность</th>
                      <th>Размер</th>
                    </tr>
                  </thead>
                  <tbody>
                    {predictionHistory.map((entry) => (
                      <tr key={entry.id}>
                        <td>#{entry.id}</td>
                        <td>{formatDateTime(entry.created_at)}</td>
                        <td>
                          <div className="file-cell">
                            <strong>{entry.filename || "unknown"}</strong>
                            <span>{entry.content_type || "n/a"}</span>
                          </div>
                        </td>
                        <td>
                          <span className="result-badge">{humanizeLabel(entry.label)}</span>
                        </td>
                        <td>{formatPercent(entry.confidence)}</td>
                        <td>{formatFileSize(entry.file_size_bytes)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p className="history-placeholder">
                  База пока пустая. Отправь изображение, и первая запись сразу появится в таблице.
                </p>
              )}
            </div>
          </section>

          <section className="database-card">
            <div className="history-header">
              <div>
                <span className="eyebrow">Inspector</span>
                <h2>Таблицы базы данных</h2>
              </div>

              <div className="history-meta">
                <strong>{databaseTables.length}</strong>
                <span>таблиц найдено</span>
              </div>
            </div>

            <p className="history-copy">
              Раздел показывает все таблицы SQLite: структуру колонок, количество строк и первые записи каждой таблицы.
            </p>

            {databaseErrorMessage ? <p className="error-banner">{databaseErrorMessage}</p> : null}

            {isDatabaseLoading ? (
              <p className="history-placeholder">Загрузка структуры базы данных...</p>
            ) : databaseTables.length > 0 ? (
              <div className="database-table-list">
                {databaseTables.map((table) => (
                  <article className="database-table-card" key={table.name}>
                    <div className="database-table-title">
                      <div>
                        <h3>{table.name}</h3>
                        <span>{table.columns.length} колонок</span>
                      </div>
                      <strong>{table.row_count} строк</strong>
                    </div>

                    <div className="column-chip-list">
                      {table.columns.map((column) => (
                        <span className="column-chip" key={`${table.name}-${column.name}`}>
                          {column.primary_key ? "PK " : ""}
                          {column.name}: {column.type}
                          {column.nullable ? "" : " *"}
                        </span>
                      ))}
                    </div>

                    <div className="table-shell">
                      {table.rows.length > 0 ? (
                        <table className="history-table database-table">
                          <thead>
                            <tr>
                              {table.columns.map((column) => (
                                <th key={`${table.name}-head-${column.name}`}>{column.name}</th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {table.rows.map((row, rowIndex) => (
                              <tr key={`${table.name}-row-${rowIndex}`}>
                                {table.columns.map((column) => (
                                  <td key={`${table.name}-${rowIndex}-${column.name}`}>
                                    {formatDatabaseValue(row[column.name])}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      ) : (
                        <p className="history-placeholder">В таблице пока нет строк.</p>
                      )}
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <p className="history-placeholder">В базе данных не найдено таблиц.</p>
            )}
          </section>
        </section>
      </main>
    </div>
  );
}

async function fetchPredictionHistory(limit) {
  const response = await fetch(`${apiBaseUrl}/predictions?limit=${limit}`);
  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.detail || "Не удалось получить историю из базы данных.");
  }

  return payload;
}

async function fetchDatabaseTables(rowLimit) {
  const response = await fetch(`${apiBaseUrl}/database/tables?row_limit=${rowLimit}`);
  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.detail || "Не удалось получить таблицы базы данных.");
  }

  return payload;
}

function humanizeLabel(label) {
  const dictionary = {
    circle: "Круг",
    triangle: "Треугольник",
    square: "Квадрат",
  };

  return dictionary[label] || label;
}

function statusLabel(status) {
  const dictionary = {
    checking: "checking",
    ready: "backend ready",
    model_missing: "training needed",
    offline: "backend offline",
  };

  return dictionary[status] || status;
}

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function formatFileSize(bytes) {
  if (bytes < 1024) {
    return `${bytes} B`;
  }

  return `${(bytes / 1024).toFixed(1)} KB`;
}

function formatDateTime(value) {
  const parsed = new Date(value);

  if (Number.isNaN(parsed.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat("ru-RU", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(parsed);
}

function formatDatabaseValue(value) {
  if (value === null || value === undefined) {
    return "NULL";
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}

export default App;
