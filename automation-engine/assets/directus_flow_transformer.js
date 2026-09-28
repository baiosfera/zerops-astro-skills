module.exports = function (data) {
  const trigger = data.$trigger;
  const payload = trigger.payload || {};

  return {
    id: crypto.randomUUID(),
    specversion: "1.0",
    type: `commerce.${trigger.collection || "entity"}.${trigger.event || "action"}`,
    source: "directus.flows",
    subject: `${trigger.collection || "entity"}.${trigger.keys?.[0] || "new"}`,
    time: new Date().toISOString(),
    datacontenttype: "application/json",
    data: payload
  };
};
