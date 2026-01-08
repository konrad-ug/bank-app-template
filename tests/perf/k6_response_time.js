import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: 10,
  iterations: 10,
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:5000";
const ACCOUNTS_URL = `${BASE_URL}/api/accounts`;

function createDeleteScenario() {
  const pesels = [];
  for (let i = 0; i < 100; i += 1) {
    const pesel = `123456${__VU}${String(i).padStart(6, "0")}`;
    pesels.push(pesel);
    const body = {
      name: "Dariusz",
      surname: "Januszewski",
      pesel,
    };
    const res = http.post(ACCOUNTS_URL, JSON.stringify(body), {
      headers: { "Content-Type": "application/json" },
      timeout: "500ms",
    });
    check(res, { "create status 201": (r) => r.status === 201 });
  }

  for (const pesel of pesels) {
    const res = http.del(`${ACCOUNTS_URL}/${pesel}`, null, { timeout: "500ms" });
    check(res, { "delete status 200": (r) => r.status === 200 });
  }
}

function transferScenario() {
  const pesel = `987654${__VU}${String(__ITER).padStart(6, "0")}`;
  const body = {
    name: "Dariusz",
    surname: "Januszewski",
    pesel,
  };

  const createRes = http.post(ACCOUNTS_URL, JSON.stringify(body), {
    headers: { "Content-Type": "application/json" },
    timeout: "1s",
  });
  check(createRes, { "create status 201": (r) => r.status === 201 });

  for (let i = 0; i < 100; i += 1) {
    const res = http.post(
      `${ACCOUNTS_URL}/${pesel}/transfer`,
      JSON.stringify({ type: "incoming", amount: 100 }),
      { headers: { "Content-Type": "application/json" }, timeout: "500ms" }
    );
    check(res, { "transfer status 200": (r) => r.status === 200 });
  }

  const accountRes = http.get(`${ACCOUNTS_URL}/${pesel}`, { timeout: "500ms" });
  check(accountRes, {
    "get status 200": (r) => r.status === 200,
    "balance correct": (r) => r.json("balance") === 100 * 100,
  });

  const deleteRes = http.del(`${ACCOUNTS_URL}/${pesel}`, null, { timeout: "500ms" });
  check(deleteRes, { "delete status 200": (r) => r.status === 200 });
}

export default function () {
  createDeleteScenario();
  transferScenario();
}
